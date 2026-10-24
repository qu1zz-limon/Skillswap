from datetime import datetime
from typing import List
from sqlalchemy import Boolean, Integer, String, DateTime, Table, Column, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.db import Base

user_skills = Table(
    "user_skills",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("skill_id", Integer, ForeignKey("skills.id", ondelete="CASCADE"), primary_key=True),
)

class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(100), nullable=False)
    owner: Mapped[str] = mapped_column(String(50), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    level: Mapped[str] = mapped_column(String(50), nullable=False)
    can_teach: Mapped[bool] = mapped_column(Boolean, nullable=False)
    want_learn: Mapped[bool] = mapped_column(Boolean, nullable=False)

    users: Mapped[List["User"]] = relationship("User", secondary=user_skills, back_populates="skills")

class Exchange(Base):
    __tablename__ = "exchanges"

    id: Mapped[int] = mapped_column(primary_key=True)
    sender_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    receiver_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    skill_id: Mapped[int] = mapped_column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending")  # pending, accepted, rejected, completed
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_exchanges")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_exchanges")
    skill = relationship("Skill")

class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    target_user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)  # Від 1 до 5
    comment: Mapped[str] = mapped_column(String(500), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    author = relationship("User", foreign_keys=[author_id], back_populates="given_reviews")
    target_user = relationship("User", foreign_keys=[target_user_id], back_populates="received_reviews")

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False)
    full_name: Mapped[str] = mapped_column(String(50), nullable=False)
    bio: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    skills: Mapped[List[Skill]] = relationship("Skill", secondary=user_skills, back_populates="users")
    sent_exchanges: Mapped[List["Exchange"]] = relationship("Exchange", foreign_keys="[Exchange.sender_id]", back_populates="sender")
    received_exchanges: Mapped[List["Exchange"]] = relationship("Exchange", foreign_keys="[Exchange.receiver_id]", back_populates="receiver")
    given_reviews: Mapped[List["Review"]] = relationship("Review", foreign_keys="[Review.author_id]", back_populates="author")
    received_reviews: Mapped[List["Review"]] = relationship("Review", foreign_keys="[Review.target_user_id]", back_populates="target_user")
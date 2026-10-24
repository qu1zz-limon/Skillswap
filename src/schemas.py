from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, model_validator, Field

class SkillLevel(str, Enum):
    beginner = "Beginner"
    intermediate = "Intermediate"
    expert = "Expert"

class SkillCategory(str, Enum):
    Data_Science = "Data Science"
    ML_Engineer = "Machine Learning Engineering"
    Software_Engineer = "Software Engineering"
    Cloud_Engineer = "Cloud Engineering"
    DevOps_Engineer = "Development Engineering"
    Database_Engineer = "Database Engineering"
    Frontend_Engineer = "Frontend Engineering"
    Backend_Engineer = "Backend Engineering"
    Nothing = "Nothing"

class SkillCreate(BaseModel):
    name: str
    description: str
    owner: str
    category: SkillCategory = Field(default=SkillCategory.Nothing)
    level: SkillLevel = Field(default=SkillLevel.beginner)
    can_teach: bool
    want_learn: bool

    @model_validator(mode="after")
    def check_fields(self):
        if self.can_teach == self.want_learn:
            raise ValueError("You can't be teacher and student in a single skill, or neither.")
        return self

    class Config:
        use_enum_values = True

class SkillUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=3, max_length=100)
    description: str | None = Field(default=None, min_length=10, max_length=500)
    owner: str | None = Field(default=None, min_length=3, max_length=100)
    category: SkillCategory | None = None
    level: SkillLevel | None = None
    can_teach: bool | None = None
    want_learn: bool | None = None

class SkillResponse(SkillCreate):
    id: int

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    email: str
    full_name: str
    bio: str
    is_active: bool = True

class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=3, max_length=100)
    email: str | None = Field(default=None, min_length=10, max_length=500)
    full_name: str | None = Field(default=None, min_length=3, max_length=100)
    bio: str | None = Field(default=None, min_length=3, max_length=100)
    created_at: datetime | None = None
    is_active: bool | None = None

class UserResponse(UserCreate):
    id: int
    created_at: datetime
    skills: List[SkillResponse] = []

    class Config:
        from_attributes = True



class ExchangeStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"
    completed = "completed"

class ExchangeCreate(BaseModel):
    receiver_id: int
    skill_id: int

class ExchangeUpdate(BaseModel):
    status: ExchangeStatus

class ExchangeResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    skill_id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class ReviewCreate(BaseModel):
    target_user_id: int
    rating: int = Field(ge=1, le=5)
    comment: str = Field(min_length=5, max_length=500)

class ReviewResponse(BaseModel):
    id: int
    author_id: int
    target_user_id: int
    rating: int
    comment: str
    created_at: datetime

    class Config:
        from_attributes = True
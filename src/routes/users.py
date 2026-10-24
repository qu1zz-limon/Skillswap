from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.schemas import UserCreate, UserUpdate, UserResponse, SkillResponse
from src.database.models import User
from src.database.db import get_db

router = APIRouter(prefix="/users", tags=["users"])

def user_not_found(user_id):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User Not Found with id {user_id}"
    )

@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        user_not_found(user_id)
    return user

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    old_user = db.get(User, user_id)
    if not old_user:
        user_not_found(user_id)

    user_update = user.model_dump(exclude_unset=True)
    for key, value in user_update.items():
        setattr(old_user, key, value)
    db.commit()
    db.refresh(old_user)
    return old_user

@router.get("/{user_id}/skills/", response_model=list[SkillResponse])
def get_user_skills(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        user_not_found(user_id)
    return user.skills
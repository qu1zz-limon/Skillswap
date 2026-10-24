from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.schemas import ReviewCreate, ReviewResponse
from src.database.models import Review, User
from src.database.db import get_db

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.get("/", response_model=List[ReviewResponse])
def get_reviews(db: Session = Depends(get_db)):
    return db.query(Review).all()


@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(review: ReviewCreate, author_id: int, db: Session = Depends(get_db)):
    target_user = db.get(User, review.target_user_id)
    if not target_user:
        raise HTTPException(status_code=404, detail="Target user not found")

    if author_id == review.target_user_id:
        raise HTTPException(status_code=400, detail="Cannot review yourself")

    new_review = Review(
        author_id=author_id,
        target_user_id=review.target_user_id,
        rating=review.rating,
        comment=review.comment
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review


@router.get("/user/{user_id}", response_model=List[ReviewResponse])
def get_user_reviews(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return db.query(Review).filter(Review.target_user_id == user_id).all()
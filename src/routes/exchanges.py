from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.schemas import ExchangeCreate, ExchangeUpdate, ExchangeResponse
from src.database.models import Exchange, User, Skill
from src.database.db import get_db

router = APIRouter(prefix="/exchanges", tags=["exchanges"])


def exchange_not_found(exchange_id: int):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Exchange with id {exchange_id} not found"
    )


@router.get("/", response_model=List[ExchangeResponse])
def get_exchanges(db: Session = Depends(get_db)):
    return db.query(Exchange).all()


@router.post("/", response_model=ExchangeResponse, status_code=status.HTTP_201_CREATED)
def create_exchange(exchange: ExchangeCreate, sender_id: int, db: Session = Depends(get_db)):
    receiver = db.get(User, exchange.receiver_id)
    if not receiver:
        raise HTTPException(status_code=404, detail="Receiver not found")

    skill = db.get(Skill, exchange.skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    if sender_id == exchange.receiver_id:
        raise HTTPException(status_code=400, detail="Cannot exchange skills with yourself")

    new_exchange = Exchange(
        sender_id=sender_id,
        receiver_id=exchange.receiver_id,
        skill_id=exchange.skill_id,
        status="pending"
    )
    db.add(new_exchange)
    db.commit()
    db.refresh(new_exchange)
    return new_exchange


@router.put("/{exchange_id}", response_model=ExchangeResponse)
def update_exchange_status(exchange_id: int, exchange_update: ExchangeUpdate, db: Session = Depends(get_db)):
    exchange = db.get(Exchange, exchange_id)
    if not exchange:
        exchange_not_found(exchange_id)

    exchange.status = exchange_update.status
    db.commit()
    db.refresh(exchange)
    return exchange
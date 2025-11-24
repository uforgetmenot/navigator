from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models.card import (
    NavigationCard,
    NavigationCardCreate,
    NavigationCardRead,
    NavigationCardUpdate,
)
from app.models.category import Category
from app.core.deps import get_current_superuser

router = APIRouter()

@router.get("/", response_model=List[NavigationCardRead])
def read_cards(
    category_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    query = select(NavigationCard)
    if category_id:
        query = query.where(NavigationCard.category_id == category_id)
    
    query = query.order_by(NavigationCard.order).offset(skip).limit(limit)
    cards = session.exec(query).all()
    return cards

@router.post("/", response_model=NavigationCardRead)
def create_card(
    card: NavigationCardCreate,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_superuser)
):
    category = session.get(Category, card.category_id)
    if not category:
        raise HTTPException(status_code=400, detail="Category not found")

    db_card = NavigationCard(**card.model_dump())
    session.add(db_card)
    session.commit()
    session.refresh(db_card)
    return db_card

@router.put("/{card_id}", response_model=NavigationCardRead)
def update_card(
    card_id: int,
    card_data: NavigationCardUpdate,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_superuser)
):
    card = session.get(NavigationCard, card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    
    card_data_dict = card_data.model_dump(exclude_unset=True)
    if "category_id" in card_data_dict:
        category = session.get(Category, card_data_dict["category_id"])
        if not category:
            raise HTTPException(status_code=400, detail="Category not found")

    for key, value in card_data_dict.items():
        setattr(card, key, value)
            
    session.add(card)
    session.commit()
    session.refresh(card)
    return card

@router.delete("/{card_id}")
def delete_card(
    card_id: int,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_superuser)
):
    card = session.get(NavigationCard, card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    session.delete(card)
    session.commit()
    return {"ok": True}

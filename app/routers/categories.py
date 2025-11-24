from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models.category import (
    Category,
    CategoryCreate,
    CategoryRead,
    CategoryUpdate,
)
from app.models.card import NavigationCard
from app.core.deps import get_current_superuser

router = APIRouter()

@router.get("/", response_model=List[CategoryRead])
def read_categories(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    categories = session.exec(select(Category).order_by(Category.order).offset(skip).limit(limit)).all()
    return categories

@router.post("/", response_model=CategoryRead)
def create_category(
    category: CategoryCreate,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_superuser)
):
    db_category = Category(**category.model_dump())
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category

@router.put("/{category_id}", response_model=CategoryRead)
def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_superuser)
):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    category_data_dict = category_data.model_dump(exclude_unset=True)

    if "slug" in category_data_dict and category_data_dict["slug"] != category.slug:
        exists = session.exec(select(Category).where(Category.slug == category_data_dict["slug"]))
        if exists.first():
            raise HTTPException(status_code=400, detail="Slug already exists")

    for key, value in category_data_dict.items():
        setattr(category, key, value)
            
    session.add(category)
    session.commit()
    session.refresh(category)
    return category

@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_superuser)
):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    # Remove related cards first to prevent orphan foreign keys
    cards = session.exec(select(NavigationCard).where(NavigationCard.category_id == category_id)).all()
    for card in cards:
        session.delete(card)

    session.delete(category)
    session.commit()
    return {"ok": True}

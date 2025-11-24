from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models.category import Category
from app.core.deps import get_current_superuser

router = APIRouter()

@router.get("/", response_model=List[Category])
def read_categories(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    categories = session.exec(select(Category).order_by(Category.order).offset(skip).limit(limit)).all()
    return categories

@router.post("/", response_model=Category)
def create_category(
    category: Category,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_superuser)
):
    db_category = Category.model_validate(category)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category

@router.put("/{category_id}", response_model=Category)
def update_category(
    category_id: int,
    category_data: Category,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_superuser)
):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    category_data_dict = category_data.model_dump(exclude_unset=True)
    for key, value in category_data_dict.items():
        if key != "id": # Prevent ID update
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
    session.delete(category)
    session.commit()
    return {"ok": True}

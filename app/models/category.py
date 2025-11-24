from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class CategoryBase(SQLModel):
    slug: str = Field(unique=True, index=True)
    label: str
    icon: str
    order: int = Field(default=0)
    active: bool = Field(default=False)


class Category(CategoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    cards: List["NavigationCard"] = Relationship(back_populates="category")


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime


class CategoryUpdate(SQLModel):
    slug: Optional[str] = None
    label: Optional[str] = None
    icon: Optional[str] = None
    order: Optional[int] = None
    active: Optional[bool] = None

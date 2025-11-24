from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from app.models.category import Category


class NavigationCardBase(SQLModel):
    category_id: int = Field(foreign_key="category.id")
    title: str
    subtitle: Optional[str] = None
    description: str
    icon: str
    icon_bg_class: str
    icon_color_class: str
    href: str
    order: int = Field(default=0)


class NavigationCard(NavigationCardBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    category: Optional[Category] = Relationship(back_populates="cards")


class NavigationCardCreate(NavigationCardBase):
    pass


class NavigationCardRead(NavigationCardBase):
    id: int
    created_at: datetime
    updated_at: datetime


class NavigationCardUpdate(SQLModel):
    category_id: Optional[int] = None
    title: Optional[str] = None
    subtitle: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    icon_bg_class: Optional[str] = None
    icon_color_class: Optional[str] = None
    href: Optional[str] = None
    order: Optional[int] = None

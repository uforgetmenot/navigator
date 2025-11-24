from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

# Forward reference for relationship
class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    slug: str = Field(unique=True, index=True)
    label: str
    icon: str
    order: int = Field(default=0)
    active: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    cards: List["NavigationCard"] = Relationship(back_populates="category")

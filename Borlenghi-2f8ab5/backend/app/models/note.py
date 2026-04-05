from typing import Optional, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.category import Category


class Note(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(default="")
    is_archived: bool = Field(default=False)
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")

    # Relationship: each note belongs to one optional category
    category: Optional["Category"] = Relationship(back_populates="notes")

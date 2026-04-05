from typing import Optional
from sqlmodel import SQLModel, Field


class NoteCreate(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = ""
    category_id: Optional[int] = None


class NoteUpdate(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = ""


class NoteOut(SQLModel):
    id: int
    title: str
    content: str
    is_archived: bool
    category_id: Optional[int] = None


class ArchiveRequest(SQLModel):
    is_archived: bool


class CategoryRequest(SQLModel):
    category_id: Optional[int] = None

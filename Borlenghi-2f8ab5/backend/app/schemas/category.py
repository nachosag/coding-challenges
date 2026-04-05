from sqlmodel import SQLModel, Field


class CategoryOut(SQLModel):
    id: int
    name: str


class CategoryCreate(SQLModel):
    name: str = Field(min_length=1, max_length=100)

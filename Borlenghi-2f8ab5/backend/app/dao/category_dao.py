from sqlmodel import Session, select
from typing import Optional
from app.models.category import Category


def get_all(session: Session) -> list[Category]:
    return list(session.exec(select(Category)).all())


def get_by_id(session: Session, category_id: int) -> Optional[Category]:
    return session.get(Category, category_id)

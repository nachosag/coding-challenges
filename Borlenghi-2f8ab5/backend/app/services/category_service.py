from sqlmodel import Session
from app.models.category import Category
from app.dao import category_dao


def get_categories(session: Session) -> list[Category]:
    return category_dao.get_all(session)

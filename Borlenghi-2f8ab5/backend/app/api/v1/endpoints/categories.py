from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.database import get_session
from app.core.auth import get_current_user
from app.models.category import Category
from app.schemas.category import CategoryOut
from app.services import category_service

router = APIRouter()


@router.get("", response_model=list[CategoryOut])
def list_categories(
    session: Session = Depends(get_session),
    _user: str = Depends(get_current_user),
) -> list[Category]:
    return category_service.get_categories(session)

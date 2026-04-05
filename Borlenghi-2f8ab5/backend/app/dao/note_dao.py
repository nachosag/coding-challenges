from sqlmodel import Session, select
from typing import Optional

from sqlmodel.sql._expression_select_cls import SelectOfScalar
from app.models.note import Note


def get_all(
    session: Session, archived: Optional[bool] = None, category_id: Optional[int] = None
) -> list[Note]:
    """Get notes with optional filters for archived status and category."""
    query: SelectOfScalar[Note] = select(Note)
    if archived is not None:
        query = query.where(Note.is_archived == archived)
    if category_id is not None:
        query = query.where(Note.category_id == category_id)
    return list(session.exec(query).all())


def get_by_id(session: Session, note_id: int) -> Optional[Note]:
    return session.get(Note, note_id)


def create(session: Session, note: Note) -> Note:
    session.add(note)
    session.commit()
    session.refresh(note)
    return note


def update(session: Session, note: Note) -> Note:
    session.add(note)
    session.commit()
    session.refresh(note)
    return note


def delete(session: Session, note: Note) -> None:
    session.delete(note)
    session.commit()

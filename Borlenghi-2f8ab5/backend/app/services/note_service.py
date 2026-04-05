from sqlmodel import Session
from typing import Optional
from fastapi import HTTPException
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteUpdate
from app.dao import note_dao, category_dao


def get_notes(
    session: Session, archived: Optional[bool] = None, category_id: Optional[int] = None
) -> list[Note]:
    return note_dao.get_all(session, archived=archived, category_id=category_id)


def get_note(session: Session, note_id: int) -> Note:
    note: Note | None = note_dao.get_by_id(session, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


def create_note(session: Session, data: NoteCreate) -> Note:
    if data.category_id is not None:
        if not category_dao.get_by_id(session, data.category_id):
            raise HTTPException(status_code=422, detail="Category not found")
    note = Note(title=data.title, content=data.content, category_id=data.category_id)
    return note_dao.create(session, note)


def update_note(session: Session, note_id: int, data: NoteUpdate) -> Note:
    note: Note = get_note(session, note_id)
    note.title = data.title
    note.content = data.content
    return note_dao.update(session, note)


def delete_note(session: Session, note_id: int) -> None:
    note: Note = get_note(session, note_id)
    note_dao.delete(session, note)


def archive_note(session: Session, note_id: int, is_archived: bool) -> Note:
    note: Note = get_note(session, note_id)
    note.is_archived = is_archived
    return note_dao.update(session, note)


def assign_category(session: Session, note_id: int, category_id: Optional[int]) -> Note:
    note: Note = get_note(session, note_id)
    if category_id is not None:
        if not category_dao.get_by_id(session, category_id):
            raise HTTPException(status_code=422, detail="Category not found")
    note.category_id = category_id
    return note_dao.update(session, note)

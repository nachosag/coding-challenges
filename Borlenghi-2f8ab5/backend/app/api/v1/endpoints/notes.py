from fastapi import APIRouter, Depends, Query
from typing import Optional
from sqlmodel import Session
from app.core.database import get_session
from app.core.auth import get_current_user
from app.models.note import Note
from app.schemas.note import (
    NoteCreate,
    NoteUpdate,
    NoteOut,
    ArchiveRequest,
    CategoryRequest,
)
from app.services import note_service

router = APIRouter()


@router.get("", response_model=list[NoteOut])
def list_notes(
    archived: Optional[bool] = Query(None),
    category_id: Optional[int] = Query(None),
    session: Session = Depends(get_session),
    _user: str = Depends(get_current_user),
) -> list[Note]:
    return note_service.get_notes(session, archived=archived, category_id=category_id)


@router.post("", response_model=NoteOut, status_code=201)
def create_note(
    data: NoteCreate,
    session: Session = Depends(get_session),
    _user: str = Depends(get_current_user),
) -> Note:
    return note_service.create_note(session, data)


@router.get("/{note_id}", response_model=NoteOut)
def get_note(
    note_id: int,
    session: Session = Depends(get_session),
    _user: str = Depends(get_current_user),
) -> Note:
    return note_service.get_note(session, note_id)


@router.put("/{note_id}", response_model=NoteOut)
def update_note(
    note_id: int,
    data: NoteUpdate,
    session: Session = Depends(get_session),
    _user: str = Depends(get_current_user),
) -> Note:
    return note_service.update_note(session, note_id, data)


@router.delete("/{note_id}", status_code=204)
def delete_note(
    note_id: int,
    session: Session = Depends(get_session),
    _user: str = Depends(get_current_user),
) -> None:
    note_service.delete_note(session, note_id)


@router.patch("/{note_id}/archive", response_model=NoteOut)
def archive_note(
    note_id: int,
    data: ArchiveRequest,
    session: Session = Depends(get_session),
    _user: str = Depends(get_current_user),
) -> Note:
    return note_service.archive_note(session, note_id, data.is_archived)


@router.patch("/{note_id}/category", response_model=NoteOut)
def assign_category(
    note_id: int,
    data: CategoryRequest,
    session: Session = Depends(get_session),
    _user: str = Depends(get_current_user),
):
    return note_service.assign_category(session, note_id, data.category_id)

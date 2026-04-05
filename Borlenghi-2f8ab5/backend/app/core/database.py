"""
SQLModel database setup and session management.

Provides engine creation, session generator, and DB initialization.
"""

from typing import Generator

from sqlalchemy import Engine
from sqlmodel import SQLModel, Session, create_engine

from app.core.config import settings

# Create the database engine
# echo=True can be enabled for SQL debugging
engine: Engine = create_engine(settings.DATABASE_URL, echo=False)


def get_session() -> Generator[Session, None, None]:
    """
    Generator dependency that yields a SQLModel Session.

    Usage in endpoints/services:
        @router.get("/notes")
        def list_notes(session: Session = Depends(get_session)):
            ...

    Yields:
        Session: A database session, automatically closed after use.
    """
    with Session(engine) as session:
        yield session


def init_db() -> None:
    """
    Initialize the database by creating all tables.

    Call this at application startup to ensure the schema exists.
    Uses SQLModel.metadata.create_all() which is idempotent.
    """
    SQLModel.metadata.create_all(engine)

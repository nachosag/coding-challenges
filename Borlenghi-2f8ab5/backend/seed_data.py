"""Seed categories and sample notes for development."""

from typing import Any, Sequence

from sqlmodel import Session, select
from app.core.database import engine, init_db
from app.models.category import Category
from app.models.note import Note


CATEGORIES: list[str] = ["Personal", "Work", "Ideas", "TODO", "Study"]

SAMPLE_NOTES: list[dict[str, Any]] = [
    {
        "title": "Welcome to Notes!",
        "content": "This is your first note. You can edit or delete it.",
        "category_id": 1,
    },
    {
        "title": "Grocery list",
        "content": "- Milk\n- Eggs\n- Bread\n- Coffee",
        "category_id": 4,
    },
    {
        "title": "Project ideas",
        "content": "- Build a CLI tool\n- Learn Rust\n- Contribute to open source",
        "category_id": 3,
    },
]


def seed() -> None:
    init_db()
    with Session(engine) as session:
        # Seed categories
        existing: Sequence[Category] = session.exec(select(Category)).all()
        if not existing:
            for name in CATEGORIES:
                session.add(Category(name=name))
            session.commit()
            print(f"Seeded {len(CATEGORIES)} categories.")

        # Seed sample notes
        existing_notes: Sequence[Note] = session.exec(select(Note)).all()
        if not existing_notes:
            for note_data in SAMPLE_NOTES:
                session.add(Note(**note_data))
            session.commit()
            print(f"Seeded {len(SAMPLE_NOTES)} notes.")
        else:
            print("Notes already exist, skipping seed.")


if __name__ == "__main__":
    seed()

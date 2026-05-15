from sqlalchemy.orm import Session
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteUpdate

def create_note(db: Session, note: NoteCreate, user_id: int) -> Note:
    """Insert a new note into the database linked to a specific user."""
    db_note = Note(title=note.title, content=note.content, user_id=user_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def get_notes_by_user(db: Session, user_id: int) -> list[Note]:
    """Get all notes that belong to a specific user."""
    return db.query(Note).filter(Note.user_id == user_id).all()

def get_note_by_id(db: Session, note_id: int) -> Note | None:
    """Get a specific note by its ID."""
    return db.query(Note).filter(Note.id == note_id).first()

def update_note(db: Session, db_note: Note, note_update: NoteUpdate) -> Note:
    """Update an existing note's fields."""
    update_data = note_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_note, key, value)
    
    db.commit()
    db.refresh(db_note)
    return db_note

def delete_note(db: Session, db_note: Note) -> None:
    """Delete a note from the database."""
    db.delete(db_note)
    db.commit()

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import note as note_schemas
from app.repositories import note_repo
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/notes", tags=["Notes"])

@router.post("/", response_model=note_schemas.NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(
    note: note_schemas.NoteCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new note for the logged-in user."""
    return note_repo.create_note(db=db, note=note, user_id=current_user.id)

@router.get("/", response_model=list[note_schemas.NoteResponse])
def get_my_notes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all notes that belong to the logged-in user."""
    return note_repo.get_notes_by_user(db=db, user_id=current_user.id)

@router.get("/{note_id}", response_model=note_schemas.NoteResponse)
def get_note(
    note_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific note by ID."""
    note = note_repo.get_note_by_id(db=db, note_id=note_id)
    
    # 1. Check if note exists
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
        
    # 2. Authorization / Ownership check (Step 6)
    if note.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this note")
        
    return note

@router.put("/{note_id}", response_model=note_schemas.NoteResponse)
def update_note(
    note_id: int, 
    note_update: note_schemas.NoteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a specific note."""
    db_note = note_repo.get_note_by_id(db=db, note_id=note_id)
    
    if not db_note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
        
    if db_note.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to modify this note")
        
    return note_repo.update_note(db=db, db_note=db_note, note_update=note_update)

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    note_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a specific note."""
    db_note = note_repo.get_note_by_id(db=db, note_id=note_id)
    
    if not db_note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
        
    if db_note.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this note")
        
    note_repo.delete_note(db=db, db_note=db_note)
    return None

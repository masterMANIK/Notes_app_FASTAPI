from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

# Base schema for shared properties
class NoteBase(BaseModel):
    title: str
    content: str

# Schema for creating a note (inherits title and content)
class NoteCreate(NoteBase):
    pass

# Schema for updating a note (all fields optional)
class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

# Schema for what we return to the user
class NoteResponse(NoteBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

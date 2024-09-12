from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class NoteBase(BaseModel):
    title: str
    content:str
    published:bool = True

class NoteCreate(NoteBase):
    pass

class Note(NoteBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

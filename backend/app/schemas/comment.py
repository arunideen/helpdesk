from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from app.models.ticket_comment import CommentSource
from app.schemas.attachment import AttachmentOut


class CommentCreate(BaseModel):
    body: str


class CommentOut(BaseModel):
    id: int
    ticket_id: int
    author_id: Optional[int]
    author_email: Optional[str]
    body: str
    source: CommentSource
    created_at: datetime
    attachments: List[AttachmentOut] = []

    class Config:
        from_attributes = True

from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from app.models.ticket import TicketCategory, TicketPriority, TicketStatus
from app.schemas.attachment import AttachmentOut


class TicketCreate(BaseModel):
    subject: str
    category: TicketCategory
    project: str
    priority: TicketPriority = TicketPriority.MEDIUM
    description: str


class TicketUpdate(BaseModel):
    subject: Optional[str] = None
    category: Optional[TicketCategory] = None
    project: Optional[str] = None
    priority: Optional[TicketPriority] = None
    status: Optional[TicketStatus] = None
    description: Optional[str] = None


class TicketOut(BaseModel):
    id: int
    subject: str
    category: TicketCategory
    project: str
    priority: TicketPriority
    status: TicketStatus
    description: str
    reporter_email: str
    reporter_id: Optional[int]
    sla_deadline: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    attachments: List[AttachmentOut] = []

    class Config:
        from_attributes = True


class TicketListOut(BaseModel):
    id: int
    subject: str
    category: TicketCategory
    project: str
    priority: TicketPriority
    status: TicketStatus
    reporter_email: str
    created_at: datetime
    updated_at: datetime
    attachment_count: int = 0

    class Config:
        from_attributes = True

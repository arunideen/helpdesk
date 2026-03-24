from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.notification import NotificationType


class NotificationOut(BaseModel):
    id: int
    user_id: int
    ticket_id: Optional[int]
    type: NotificationType
    message: Optional[str]
    read: bool
    created_at: datetime

    class Config:
        from_attributes = True

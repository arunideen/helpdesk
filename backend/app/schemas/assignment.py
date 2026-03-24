from datetime import datetime

from pydantic import BaseModel


class AssignmentCreate(BaseModel):
    agent_id: int


class AssignmentOut(BaseModel):
    id: int
    ticket_id: int
    agent_id: int
    assigned_at: datetime

    class Config:
        from_attributes = True

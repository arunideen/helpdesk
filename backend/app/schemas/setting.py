from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SettingOut(BaseModel):
    id: int
    key: str
    value: str
    category: str
    label: str
    description: Optional[str]
    value_type: str
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class SettingUpdate(BaseModel):
    value: str


class SettingBulkUpdate(BaseModel):
    settings: dict[str, str]  # key -> value

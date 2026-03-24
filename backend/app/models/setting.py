from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, func

from app.database import Base


class Setting(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, nullable=False, index=True)
    value = Column(Text, nullable=False, default="")
    category = Column(String(50), nullable=False, default="general")
    label = Column(String(200), nullable=False, default="")
    description = Column(Text, nullable=True)
    value_type = Column(String(20), nullable=False, default="string")  # string, int, bool, password
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

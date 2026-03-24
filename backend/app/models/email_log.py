import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, Enum, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class EmailDirection(str, enum.Enum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"


class EmailLog(Base):
    __tablename__ = "email_logs"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=True, index=True)
    message_id = Column(String(500), unique=True, nullable=False, index=True)
    in_reply_to = Column(String(500), nullable=True)
    sender_email = Column(String(255), nullable=False)
    direction = Column(Enum(EmailDirection), nullable=False)
    subject = Column(String(500), nullable=True)
    raw_content = Column(Text, nullable=True)
    parsed_ok = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    ticket = relationship("Ticket", back_populates="email_logs")

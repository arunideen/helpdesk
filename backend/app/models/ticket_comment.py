import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, Enum, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class CommentSource(str, enum.Enum):
    EMAIL = "email"
    WEB = "web"


class TicketComment(Base):
    __tablename__ = "ticket_comments"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False, index=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    author_email = Column(String(255), nullable=True)
    body = Column(Text, nullable=False)
    source = Column(Enum(CommentSource), nullable=False, default=CommentSource.WEB)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    ticket = relationship("Ticket", back_populates="comments")
    author = relationship("User", back_populates="comments")
    attachments = relationship("Attachment", back_populates="comment")

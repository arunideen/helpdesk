from sqlalchemy import Column, Integer, Enum

from app.database import Base
from app.models.ticket import TicketPriority


class SLAPolicy(Base):
    __tablename__ = "sla_policies"

    id = Column(Integer, primary_key=True, index=True)
    priority = Column(Enum(TicketPriority), unique=True, nullable=False)
    max_response_hours = Column(Integer, nullable=False)
    max_resolution_hours = Column(Integer, nullable=False)

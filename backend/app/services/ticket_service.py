import logging
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.orm import Session

from app.models.ticket import Ticket, TicketCategory, TicketPriority, TicketStatus
from app.models.ticket_assignment import TicketAssignment
from app.models.ticket_comment import TicketComment, CommentSource
from app.models.attachment import Attachment
from app.models.sla_policy import SLAPolicy
from app.models.notification import Notification, NotificationType
from app.schemas.ticket import TicketCreate, TicketUpdate

logger = logging.getLogger(__name__)


def create_ticket(
    db: Session,
    data: TicketCreate,
    reporter_email: str,
    reporter_id: Optional[int] = None,
) -> Ticket:
    """Create a new ticket and set SLA deadline."""
    sla = db.query(SLAPolicy).filter(SLAPolicy.priority == data.priority).first()
    sla_deadline = None
    if sla:
        sla_deadline = datetime.utcnow() + timedelta(hours=sla.max_resolution_hours)

    ticket = Ticket(
        subject=data.subject,
        category=data.category,
        project=data.project,
        priority=data.priority,
        status=TicketStatus.OPEN,
        description=data.description,
        reporter_email=reporter_email,
        reporter_id=reporter_id,
        sla_deadline=sla_deadline,
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


def get_ticket(db: Session, ticket_id: int) -> Optional[Ticket]:
    return db.query(Ticket).filter(Ticket.id == ticket_id).first()


def list_tickets(
    db: Session,
    status: Optional[TicketStatus] = None,
    priority: Optional[TicketPriority] = None,
    category: Optional[TicketCategory] = None,
    project: Optional[str] = None,
    reporter_email: Optional[str] = None,
    assigned_agent_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 50,
) -> tuple[list[Ticket], int]:
    """List tickets with optional filters. Returns (tickets, total_count)."""
    query = db.query(Ticket)

    if status:
        query = query.filter(Ticket.status == status)
    if priority:
        query = query.filter(Ticket.priority == priority)
    if category:
        query = query.filter(Ticket.category == category)
    if project:
        query = query.filter(Ticket.project.ilike(f"%{project}%"))
    if reporter_email:
        query = query.filter(Ticket.reporter_email == reporter_email)
    if assigned_agent_id:
        query = query.join(TicketAssignment).filter(
            TicketAssignment.agent_id == assigned_agent_id
        )

    total = query.count()
    tickets = query.order_by(Ticket.created_at.desc()).offset(skip).limit(limit).all()
    return tickets, total


def update_ticket(db: Session, ticket: Ticket, data: TicketUpdate) -> Ticket:
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(ticket, field, value)
    db.commit()
    db.refresh(ticket)
    return ticket


def assign_ticket(db: Session, ticket_id: int, agent_id: int) -> TicketAssignment:
    assignment = TicketAssignment(
        ticket_id=ticket_id,
        agent_id=agent_id,
    )
    db.add(assignment)

    # Update ticket status to in_progress if it's open
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if ticket and ticket.status == TicketStatus.OPEN:
        ticket.status = TicketStatus.IN_PROGRESS

    db.commit()
    db.refresh(assignment)
    return assignment


def add_comment(
    db: Session,
    ticket_id: int,
    body: str,
    author_id: Optional[int] = None,
    author_email: Optional[str] = None,
    source: CommentSource = CommentSource.WEB,
) -> TicketComment:
    comment = TicketComment(
        ticket_id=ticket_id,
        author_id=author_id,
        author_email=author_email,
        body=body,
        source=source,
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def get_comments(db: Session, ticket_id: int) -> list[TicketComment]:
    return (
        db.query(TicketComment)
        .filter(TicketComment.ticket_id == ticket_id)
        .order_by(TicketComment.created_at.asc())
        .all()
    )

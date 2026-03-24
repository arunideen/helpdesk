from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User, UserRole
from app.models.ticket import TicketCategory, TicketPriority, TicketStatus
from app.schemas.ticket import TicketCreate, TicketUpdate, TicketOut, TicketListOut
from app.schemas.comment import CommentCreate, CommentOut
from app.schemas.assignment import AssignmentCreate, AssignmentOut
from app.schemas.attachment import AttachmentOut
from app.services.ticket_service import (
    create_ticket,
    get_ticket,
    list_tickets,
    update_ticket,
    assign_ticket,
    add_comment,
    get_comments,
)
from app.utils.auth import get_current_user, require_roles

router = APIRouter(prefix="/api/tickets", tags=["tickets"])


@router.post("/", response_model=TicketOut, status_code=status.HTTP_201_CREATED)
def create_new_ticket(
    data: TicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ticket = create_ticket(db, data, current_user.email, current_user.id)
    return ticket


@router.get("/", response_model=dict)
def list_all_tickets(
    status_filter: Optional[TicketStatus] = Query(None, alias="status"),
    priority: Optional[TicketPriority] = None,
    category: Optional[TicketCategory] = None,
    project: Optional[str] = None,
    assigned_to: Optional[int] = None,
    skip: int = 0,
    limit: int = Query(50, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Clients can only see their own tickets
    reporter_email = None
    if current_user.role == UserRole.CLIENT:
        reporter_email = current_user.email

    tickets, total = list_tickets(
        db,
        status=status_filter,
        priority=priority,
        category=category,
        project=project,
        reporter_email=reporter_email,
        assigned_agent_id=assigned_to,
        skip=skip,
        limit=limit,
    )

    items = []
    for t in tickets:
        item = TicketListOut.model_validate(t)
        item.attachment_count = len(t.attachments)
        items.append(item)

    return {"items": items, "total": total, "skip": skip, "limit": limit}


@router.get("/{ticket_id}", response_model=TicketOut)
def get_single_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ticket = get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Clients can only view their own tickets
    if current_user.role == UserRole.CLIENT and ticket.reporter_email != current_user.email:
        raise HTTPException(status_code=403, detail="Access denied")

    return ticket


@router.put("/{ticket_id}", response_model=TicketOut)
def update_existing_ticket(
    ticket_id: int,
    data: TicketUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.MANAGER, UserRole.AGENT)),
):
    ticket = get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return update_ticket(db, ticket, data)


# Assignments
@router.post("/{ticket_id}/assign", response_model=AssignmentOut, status_code=status.HTTP_201_CREATED)
def assign_agent(
    ticket_id: int,
    data: AssignmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.MANAGER, UserRole.AGENT)),
):
    ticket = get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    agent = db.query(User).filter(User.id == data.agent_id, User.role == UserRole.AGENT).first()
    if not agent:
        raise HTTPException(status_code=400, detail="Invalid agent ID")

    assignment = assign_ticket(db, ticket_id, data.agent_id)
    return assignment


# Comments
@router.post("/{ticket_id}/comments", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
def create_comment(
    ticket_id: int,
    data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ticket = get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    if current_user.role == UserRole.CLIENT and ticket.reporter_email != current_user.email:
        raise HTTPException(status_code=403, detail="Access denied")

    comment = add_comment(
        db, ticket_id, data.body,
        author_id=current_user.id,
        author_email=current_user.email,
    )
    return comment


@router.get("/{ticket_id}/comments", response_model=List[CommentOut])
def list_comments(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ticket = get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    if current_user.role == UserRole.CLIENT and ticket.reporter_email != current_user.email:
        raise HTTPException(status_code=403, detail="Access denied")

    return get_comments(db, ticket_id)


# Attachments
@router.get("/{ticket_id}/attachments", response_model=List[AttachmentOut])
def list_attachments(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ticket = get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    if current_user.role == UserRole.CLIENT and ticket.reporter_email != current_user.email:
        raise HTTPException(status_code=403, detail="Access denied")

    return ticket.attachments

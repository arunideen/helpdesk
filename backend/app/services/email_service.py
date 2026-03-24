import logging
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.config import settings
from app.models.email_log import EmailLog, EmailDirection
from app.models.attachment import Attachment
from app.models.ticket import Ticket
from app.models.ticket_comment import TicketComment, CommentSource
from app.email.parser import ParsedEmail, parse_email_content
from app.email.imap_client import fetch_unread_emails
from app.email.smtp_client import send_format_error_reply
from app.schemas.ticket import TicketCreate
from app.services.ticket_service import create_ticket, add_comment
from app.utils.storage import save_attachment, is_allowed_extension, is_within_size_limit

logger = logging.getLogger(__name__)


def is_duplicate(db: Session, message_id: str) -> bool:
    """Check if an email with this message_id has already been processed."""
    return db.query(EmailLog).filter(EmailLog.message_id == message_id).first() is not None


def can_send_auto_reply(db: Session, sender_email: str) -> bool:
    """Check rate limit: max 1 auto-reply per sender within the cooldown period."""
    cutoff = datetime.utcnow() - timedelta(seconds=settings.AUTO_REPLY_COOLDOWN_SECONDS)
    recent = (
        db.query(EmailLog)
        .filter(
            EmailLog.sender_email == sender_email,
            EmailLog.direction == EmailDirection.OUTBOUND,
            EmailLog.created_at > cutoff,
        )
        .first()
    )
    return recent is None


def log_email(
    db: Session,
    message_id: str,
    sender_email: str,
    direction: EmailDirection,
    subject: str = "",
    raw_content: str = "",
    parsed_ok: bool = False,
    ticket_id: int = None,
) -> EmailLog:
    log = EmailLog(
        message_id=message_id,
        sender_email=sender_email,
        direction=direction,
        subject=subject,
        raw_content=raw_content,
        parsed_ok=parsed_ok,
        ticket_id=ticket_id,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def save_parsed_attachments(db: Session, parsed: ParsedEmail, ticket_id: int, comment_id: int = None) -> list[Attachment]:
    """Save valid attachments from a parsed email to storage and database."""
    saved = []
    total_size = 0

    for att in parsed.attachments:
        if not is_allowed_extension(att.filename):
            logger.warning("Skipping attachment '%s': unsupported extension", att.filename)
            continue

        if not is_within_size_limit(att.size_bytes):
            logger.warning(
                "Skipping attachment '%s': exceeds %d MB limit",
                att.filename,
                settings.MAX_ATTACHMENT_SIZE_MB,
            )
            continue

        total_size += att.size_bytes
        if total_size > settings.MAX_TOTAL_ATTACHMENT_SIZE_MB * 1024 * 1024:
            logger.warning("Skipping remaining attachments: total size exceeds %d MB", settings.MAX_TOTAL_ATTACHMENT_SIZE_MB)
            break

        stored_filename, storage_path = save_attachment(att.content, att.filename)
        attachment = Attachment(
            ticket_id=ticket_id,
            comment_id=comment_id,
            filename=stored_filename,
            original_filename=att.filename,
            content_type=att.content_type,
            size_bytes=att.size_bytes,
            storage_path=storage_path,
        )
        db.add(attachment)
        saved.append(attachment)

    if saved:
        db.commit()
    return saved


def find_ticket_by_email_thread(db: Session, in_reply_to: str, references: str) -> Ticket:
    """Try to find an existing ticket by In-Reply-To or References headers."""
    if in_reply_to:
        email_log = (
            db.query(EmailLog)
            .filter(EmailLog.message_id == in_reply_to, EmailLog.ticket_id.isnot(None))
            .first()
        )
        if email_log:
            return db.query(Ticket).filter(Ticket.id == email_log.ticket_id).first()

    if references:
        for ref in references.split():
            ref = ref.strip()
            if ref:
                email_log = (
                    db.query(EmailLog)
                    .filter(EmailLog.message_id == ref, EmailLog.ticket_id.isnot(None))
                    .first()
                )
                if email_log:
                    return db.query(Ticket).filter(Ticket.id == email_log.ticket_id).first()

    return None


def process_incoming_emails(db: Session) -> dict:
    """Main entry point: fetch, parse, validate, and process all unread emails."""
    stats = {"processed": 0, "tickets_created": 0, "replies_added": 0, "auto_replies_sent": 0, "duplicates_skipped": 0}

    raw_emails = fetch_unread_emails()
    logger.info("Fetched %d unread emails", len(raw_emails))

    for raw in raw_emails:
        stats["processed"] += 1
        message_id = raw["message_id"]

        # Deduplication
        if is_duplicate(db, message_id):
            logger.info("Skipping duplicate email: %s", message_id)
            stats["duplicates_skipped"] += 1
            continue

        # Parse email
        parsed = parse_email_content(
            message_id=message_id,
            sender_email=raw["sender_email"],
            subject=raw["subject"],
            body=raw["body"],
            attachments=raw["attachments"],
            in_reply_to=raw.get("in_reply_to"),
            references=raw.get("references"),
        )

        # Check if this is a reply to an existing ticket
        existing_ticket = None
        if parsed.in_reply_to or parsed.references:
            existing_ticket = find_ticket_by_email_thread(
                db, parsed.in_reply_to, parsed.references
            )

        if existing_ticket:
            # Add as a comment on the existing ticket
            comment = add_comment(
                db=db,
                ticket_id=existing_ticket.id,
                body=parsed.body_raw,
                author_email=parsed.sender_email,
                source=CommentSource.EMAIL,
            )
            save_parsed_attachments(db, parsed, existing_ticket.id, comment.id)
            log_email(
                db, message_id, parsed.sender_email,
                EmailDirection.INBOUND, parsed.subject,
                raw.get("raw", ""), True, existing_ticket.id,
            )
            stats["replies_added"] += 1
            continue

        # Validate format for new tickets
        if not parsed.is_valid:
            log_email(
                db, message_id, parsed.sender_email,
                EmailDirection.INBOUND, parsed.subject,
                raw.get("raw", ""), False,
            )

            if can_send_auto_reply(db, parsed.sender_email):
                sent = send_format_error_reply(
                    to_email=parsed.sender_email,
                    original_subject=parsed.subject,
                    errors=parsed.errors,
                    original_message_id=message_id,
                )
                if sent:
                    log_email(
                        db, f"auto-reply-{message_id}", parsed.sender_email,
                        EmailDirection.OUTBOUND,
                        f"RE: {parsed.subject} — Format Required",
                    )
                    stats["auto_replies_sent"] += 1
            else:
                logger.info("Rate-limited auto-reply for %s", parsed.sender_email)
            continue

        # Create new ticket
        ticket_data = TicketCreate(
            subject=f"[{parsed.category.value}] {parsed.summary}",
            category=parsed.category,
            project=parsed.project,
            priority=parsed.priority,
            description=parsed.description,
        )
        ticket = create_ticket(db, ticket_data, parsed.sender_email)
        save_parsed_attachments(db, parsed, ticket.id)
        log_email(
            db, message_id, parsed.sender_email,
            EmailDirection.INBOUND, parsed.subject,
            raw.get("raw", ""), True, ticket.id,
        )
        stats["tickets_created"] += 1
        logger.info("Created ticket #%d from email %s", ticket.id, message_id)

    return stats

import re
import logging
from dataclasses import dataclass, field
from typing import Optional, List

from app.models.ticket import TicketCategory, TicketPriority

logger = logging.getLogger(__name__)

VALID_CATEGORIES = {c.value.lower(): c for c in TicketCategory}
VALID_PRIORITIES = {p.value.lower(): p for p in TicketPriority}

SUBJECT_PATTERN = re.compile(r"^\[(\w+)\]\s+(.+)$")


@dataclass
class ParsedAttachment:
    filename: str
    content_type: str
    content: bytes
    size_bytes: int


@dataclass
class ParsedEmail:
    message_id: str
    sender_email: str
    subject: str
    in_reply_to: Optional[str] = None
    references: Optional[str] = None
    # Parsed fields
    category: Optional[TicketCategory] = None
    summary: Optional[str] = None
    project: Optional[str] = None
    priority: Optional[TicketPriority] = None
    description: Optional[str] = None
    body_raw: str = ""
    attachments: List[ParsedAttachment] = field(default_factory=list)
    # Validation
    is_valid: bool = False
    errors: List[str] = field(default_factory=list)


def parse_subject(subject: str) -> tuple[Optional[TicketCategory], Optional[str], list[str]]:
    """Parse the subject line for [Category] and summary."""
    errors = []
    subject = subject.strip()

    # Strip RE:/FW: prefixes for reply detection
    clean_subject = re.sub(r"^(RE|FW|Fwd):\s*", "", subject, flags=re.IGNORECASE).strip()

    match = SUBJECT_PATTERN.match(clean_subject)
    if not match:
        errors.append("Subject must follow format: [Category] Short summary")
        return None, None, errors

    category_str = match.group(1).lower()
    summary = match.group(2).strip()

    if category_str not in VALID_CATEGORIES:
        valid = ", ".join([c.value for c in TicketCategory])
        errors.append(f"Invalid category '{match.group(1)}'. Valid categories: {valid}")
        return None, summary, errors

    return VALID_CATEGORIES[category_str], summary, errors


def parse_body(body: str) -> tuple[Optional[str], Optional[TicketPriority], Optional[str], list[str]]:
    """Parse the body for Project, Priority, and Description fields."""
    errors = []
    project = None
    priority = None
    description = None

    lines = body.strip().splitlines()

    project_pattern = re.compile(r"^Project:\s*(.+)$", re.IGNORECASE)
    priority_pattern = re.compile(r"^Priority:\s*(.+)$", re.IGNORECASE)
    desc_pattern = re.compile(r"^Description:\s*(.*)$", re.IGNORECASE)

    desc_started = False
    desc_lines = []

    for line in lines:
        if desc_started:
            desc_lines.append(line)
            continue

        pm = project_pattern.match(line.strip())
        if pm:
            project = pm.group(1).strip()
            continue

        prm = priority_pattern.match(line.strip())
        if prm:
            pri_str = prm.group(1).strip().lower()
            if pri_str in VALID_PRIORITIES:
                priority = VALID_PRIORITIES[pri_str]
            else:
                valid = ", ".join([p.value for p in TicketPriority])
                errors.append(f"Invalid priority '{prm.group(1).strip()}'. Valid priorities: {valid}")
            continue

        dm = desc_pattern.match(line.strip())
        if dm:
            desc_started = True
            first_line = dm.group(1).strip()
            if first_line:
                desc_lines.append(first_line)
            continue

    if not project:
        errors.append("Body must contain 'Project: <project-name>'")
    if not priority and not any("priority" in e.lower() for e in errors):
        errors.append("Body must contain 'Priority: Low | Medium | High | Critical'")
    if not desc_started:
        errors.append("Body must contain 'Description:' followed by details")
    elif not desc_lines or not "".join(desc_lines).strip():
        errors.append("Description cannot be empty")

    if desc_lines:
        description = "\n".join(desc_lines).strip()

    return project, priority, description, errors


def parse_email_content(
    message_id: str,
    sender_email: str,
    subject: str,
    body: str,
    attachments: List[ParsedAttachment],
    in_reply_to: Optional[str] = None,
    references: Optional[str] = None,
) -> ParsedEmail:
    """Parse and validate a full email into a ParsedEmail object."""
    parsed = ParsedEmail(
        message_id=message_id,
        sender_email=sender_email,
        subject=subject,
        in_reply_to=in_reply_to,
        references=references,
        body_raw=body,
        attachments=attachments,
    )

    category, summary, subject_errors = parse_subject(subject)
    parsed.category = category
    parsed.summary = summary
    parsed.errors.extend(subject_errors)

    project, priority, description, body_errors = parse_body(body)
    parsed.project = project
    parsed.priority = priority
    parsed.description = description
    parsed.errors.extend(body_errors)

    parsed.is_valid = len(parsed.errors) == 0
    return parsed

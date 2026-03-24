import email
import imaplib
import logging
from email.header import decode_header
from email.utils import parseaddr
from typing import List, Optional

from app.config import settings
from app.email.parser import ParsedAttachment

logger = logging.getLogger(__name__)


def decode_header_value(value: str) -> str:
    """Decode an email header value that may be encoded."""
    if not value:
        return ""
    decoded_parts = decode_header(value)
    result = []
    for part, charset in decoded_parts:
        if isinstance(part, bytes):
            result.append(part.decode(charset or "utf-8", errors="replace"))
        else:
            result.append(part)
    return "".join(result)


def extract_body(msg: email.message.Message) -> str:
    """Extract the plain text body from an email message."""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            disposition = str(part.get("Content-Disposition", ""))
            if content_type == "text/plain" and "attachment" not in disposition:
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset() or "utf-8"
                    return payload.decode(charset, errors="replace")
        # Fallback to HTML if no plain text
        for part in msg.walk():
            content_type = part.get_content_type()
            disposition = str(part.get("Content-Disposition", ""))
            if content_type == "text/html" and "attachment" not in disposition:
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset() or "utf-8"
                    return payload.decode(charset, errors="replace")
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            charset = msg.get_content_charset() or "utf-8"
            return payload.decode(charset, errors="replace")
    return ""


def extract_attachments(msg: email.message.Message) -> List[ParsedAttachment]:
    """Extract all attachments from an email message."""
    attachments = []
    if not msg.is_multipart():
        return attachments

    for part in msg.walk():
        disposition = str(part.get("Content-Disposition", ""))
        if "attachment" not in disposition and "inline" not in disposition:
            continue
        content_type = part.get_content_type()
        # Skip text/plain and text/html body parts
        if content_type in ("text/plain", "text/html") and "attachment" not in disposition:
            continue

        filename = part.get_filename()
        if filename:
            filename = decode_header_value(filename)
        else:
            filename = f"attachment_{len(attachments)}"

        payload = part.get_payload(decode=True)
        if payload:
            attachments.append(ParsedAttachment(
                filename=filename,
                content_type=content_type or "application/octet-stream",
                content=payload,
                size_bytes=len(payload),
            ))

    return attachments


def fetch_unread_emails() -> list[dict]:
    """Connect to IMAP mailbox and fetch all unread emails. Returns list of raw email data dicts."""
    if not settings.IMAP_HOST or not settings.IMAP_USER:
        logger.warning("IMAP not configured, skipping email fetch")
        return []

    results = []
    try:
        if settings.IMAP_USE_SSL:
            conn = imaplib.IMAP4_SSL(settings.IMAP_HOST, settings.IMAP_PORT)
        else:
            conn = imaplib.IMAP4(settings.IMAP_HOST, settings.IMAP_PORT)

        conn.login(settings.IMAP_USER, settings.IMAP_PASSWORD)
        conn.select("INBOX")

        status, message_ids = conn.search(None, "UNSEEN")
        if status != "OK":
            logger.error("IMAP search failed: %s", status)
            conn.logout()
            return []

        for msg_id in message_ids[0].split():
            try:
                status, msg_data = conn.fetch(msg_id, "(RFC822)")
                if status != "OK":
                    continue

                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)

                message_id = msg.get("Message-ID", "").strip()
                subject = decode_header_value(msg.get("Subject", ""))
                sender_name, sender_email_addr = parseaddr(msg.get("From", ""))
                in_reply_to = msg.get("In-Reply-To", "").strip() or None
                references = msg.get("References", "").strip() or None

                body = extract_body(msg)
                attachments = extract_attachments(msg)

                results.append({
                    "message_id": message_id,
                    "sender_email": sender_email_addr,
                    "subject": subject,
                    "body": body,
                    "in_reply_to": in_reply_to,
                    "references": references,
                    "attachments": attachments,
                    "raw": raw_email.decode("utf-8", errors="replace"),
                })

                # Mark as seen
                conn.store(msg_id, "+FLAGS", "\\Seen")

            except Exception as e:
                logger.exception("Error processing email %s: %s", msg_id, e)
                continue

        conn.logout()
    except Exception as e:
        logger.exception("IMAP connection error: %s", e)

    return results

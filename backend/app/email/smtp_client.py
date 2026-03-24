import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.config import settings

logger = logging.getLogger(__name__)

FORMAT_TEMPLATE = """Hi,

Your email could not be processed as a helpdesk ticket because it doesn't
follow the required format. Please resend using this template:

Subject: [Category] Short summary
  Categories: Bug, Feature, Access, Infra, General, Urgent

Body:
  Project: <project-name>
  Priority: Low | Medium | High | Critical
  Description:
  <your detailed description>

Note: You may attach files (max {max_size} MB each, {max_total} MB total).
Supported types: {allowed_types}

Errors found in your email:
{errors}

Thank you,
{bot_name}
"""


def send_format_error_reply(
    to_email: str,
    original_subject: str,
    errors: list[str],
    original_message_id: str = "",
) -> bool:
    """Send an auto-reply informing the sender about format errors."""
    if not settings.SMTP_HOST or not settings.SMTP_USER:
        logger.warning("SMTP not configured, skipping auto-reply")
        return False

    error_list = "\n".join(f"  - {e}" for e in errors)
    body = FORMAT_TEMPLATE.format(
        max_size=settings.MAX_ATTACHMENT_SIZE_MB,
        max_total=settings.MAX_TOTAL_ATTACHMENT_SIZE_MB,
        allowed_types=settings.ALLOWED_EXTENSIONS,
        errors=error_list,
        bot_name=settings.SMTP_FROM_NAME,
    )

    msg = MIMEMultipart()
    msg["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_FROM_EMAIL}>"
    msg["To"] = to_email
    msg["Subject"] = f"RE: {original_subject} — Format Required"
    if original_message_id:
        msg["In-Reply-To"] = original_message_id
        msg["References"] = original_message_id
    msg.attach(MIMEText(body, "plain"))

    try:
        if settings.SMTP_USE_TLS:
            server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
            server.ehlo()
            server.starttls()
        else:
            server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)

        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        logger.info("Sent format error reply to %s", to_email)
        return True
    except Exception as e:
        logger.exception("Failed to send auto-reply to %s: %s", to_email, e)
        return False

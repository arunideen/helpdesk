import logging

from app.workers.celery_app import celery_app
from app.database import SessionLocal
from app.services.email_service import process_incoming_emails

logger = logging.getLogger(__name__)


@celery_app.task(name="app.workers.tasks.poll_emails")
def poll_emails():
    """Celery task: poll the IMAP mailbox for new emails and process them."""
    db = SessionLocal()
    try:
        stats = process_incoming_emails(db)
        logger.info("Email poll complete: %s", stats)
        return stats
    except Exception as e:
        logger.exception("Error during email poll: %s", e)
        raise
    finally:
        db.close()

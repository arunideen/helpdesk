from celery import Celery

from app.config import settings

celery_app = Celery(
    "helpdesk",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    beat_schedule={
        "poll-emails": {
            "task": "app.workers.tasks.poll_emails",
            "schedule": settings.IMAP_POLL_INTERVAL_SECONDS,
        },
    },
)

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Helpdesk System"
    DEBUG: bool = False
    SECRET_KEY: str = "change-me-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Database
    DATABASE_URL: str = "postgresql://helpdesk:helpdesk@localhost:5432/helpdesk"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # IMAP
    IMAP_HOST: str = ""
    IMAP_PORT: int = 993
    IMAP_USER: str = ""
    IMAP_PASSWORD: str = ""
    IMAP_USE_SSL: bool = True
    IMAP_POLL_INTERVAL_SECONDS: int = 120

    # SMTP
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_USE_TLS: bool = True
    SMTP_FROM_EMAIL: str = "support@company.com"
    SMTP_FROM_NAME: str = "Helpdesk Bot"

    # Attachments
    UPLOAD_DIR: str = "uploads"
    MAX_ATTACHMENT_SIZE_MB: int = 10
    MAX_TOTAL_ATTACHMENT_SIZE_MB: int = 25
    ALLOWED_EXTENSIONS: str = "png,jpg,jpeg,gif,pdf,doc,docx,xls,xlsx,csv,txt,zip,tar.gz,log"

    # S3 (optional, for production)
    S3_ENDPOINT: Optional[str] = None
    S3_BUCKET: Optional[str] = None
    S3_ACCESS_KEY: Optional[str] = None
    S3_SECRET_KEY: Optional[str] = None

    # Auto-reply rate limit
    AUTO_REPLY_COOLDOWN_SECONDS: int = 3600

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

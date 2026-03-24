import os
import uuid
from pathlib import Path

from app.config import settings


def get_upload_dir() -> Path:
    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)
    return upload_dir


def save_attachment(content: bytes, original_filename: str) -> tuple[str, str]:
    """Save an attachment to local storage. Returns (stored_filename, storage_path)."""
    ext = Path(original_filename).suffix
    stored_filename = f"{uuid.uuid4().hex}{ext}"
    upload_dir = get_upload_dir()
    storage_path = upload_dir / stored_filename
    storage_path.write_bytes(content)
    return stored_filename, str(storage_path)


def get_allowed_extensions() -> set[str]:
    raw = settings.ALLOWED_EXTENSIONS.split(",")
    extensions = set()
    for ext in raw:
        ext = ext.strip().lower()
        if not ext.startswith("."):
            ext = f".{ext}"
        extensions.add(ext)
    return extensions


def is_allowed_extension(filename: str) -> bool:
    ext = Path(filename).suffix.lower()
    if filename.lower().endswith(".tar.gz"):
        ext = ".tar.gz"
    return ext in get_allowed_extensions()


def is_within_size_limit(size_bytes: int) -> bool:
    return size_bytes <= settings.MAX_ATTACHMENT_SIZE_MB * 1024 * 1024

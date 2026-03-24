import os
import uuid
from pathlib import Path
from typing import List

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.user import User
from app.models.attachment import Attachment
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api/attachments", tags=["attachments"])

ALLOWED_EXTENSIONS = set(settings.ALLOWED_EXTENSIONS.split(","))
MAX_SIZE = settings.MAX_ATTACHMENT_SIZE_MB * 1024 * 1024
MAX_TOTAL = settings.MAX_TOTAL_ATTACHMENT_SIZE_MB * 1024 * 1024


def _get_ext(filename: str) -> str:
    parts = filename.rsplit(".", 1)
    return parts[-1].lower() if len(parts) > 1 else ""


@router.post("/upload", response_model=dict, status_code=201)
async def upload_attachments(
    ticket_id: int = Form(...),
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")

    upload_dir = Path(settings.UPLOAD_DIR) / str(ticket_id)
    upload_dir.mkdir(parents=True, exist_ok=True)

    total_size = 0
    created = []

    for f in files:
        ext = _get_ext(f.filename or "")
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"File type '.{ext}' not allowed. Allowed: {settings.ALLOWED_EXTENSIONS}",
            )

        content = await f.read()
        size = len(content)

        if size > MAX_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File '{f.filename}' exceeds max size of {settings.MAX_ATTACHMENT_SIZE_MB}MB",
            )

        total_size += size
        if total_size > MAX_TOTAL:
            raise HTTPException(
                status_code=400,
                detail=f"Total attachment size exceeds {settings.MAX_TOTAL_ATTACHMENT_SIZE_MB}MB",
            )

        stored_name = f"{uuid.uuid4().hex}.{ext}" if ext else uuid.uuid4().hex
        file_path = upload_dir / stored_name

        with open(file_path, "wb") as out:
            out.write(content)

        attachment = Attachment(
            ticket_id=ticket_id,
            filename=stored_name,
            original_filename=f.filename or stored_name,
            content_type=f.content_type or "application/octet-stream",
            size_bytes=size,
            storage_path=str(file_path),
        )
        db.add(attachment)
        db.flush()
        created.append({
            "id": attachment.id,
            "original_filename": attachment.original_filename,
            "size_bytes": attachment.size_bytes,
        })

    db.commit()
    return {"uploaded": len(created), "attachments": created}


@router.get("/{attachment_id}/download")
def download_attachment(
    attachment_id: int,
    token: str = None,
    db: Session = Depends(get_db),
):
    # Authenticate via query param token (for browser <a> links)
    if not token:
        raise HTTPException(status_code=401, detail="Token required")

    from jose import JWTError, jwt as jose_jwt
    from app.config import settings as app_settings
    try:
        payload = jose_jwt.decode(token, app_settings.SECRET_KEY, algorithms=["HS256"])
        sub = payload.get("sub")
        if sub is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user_id = int(sub)
    except (JWTError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Invalid token")

    attachment = db.query(Attachment).filter(Attachment.id == attachment_id).first()
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")

    file_path = Path(attachment.storage_path)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found on disk")

    return FileResponse(
        path=str(file_path),
        filename=attachment.original_filename,
        media_type=attachment.content_type,
    )

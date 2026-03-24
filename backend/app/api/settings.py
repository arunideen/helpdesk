from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.setting import Setting
from app.models.user import User, UserRole
from app.schemas.setting import SettingOut, SettingBulkUpdate
from app.utils.auth import require_roles

router = APIRouter(prefix="/api/settings", tags=["settings"])


@router.get("/", response_model=List[SettingOut])
def list_settings(
    category: str = None,
    current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.MANAGER)),
    db: Session = Depends(get_db),
):
    query = db.query(Setting)
    if category:
        query = query.filter(Setting.category == category)
    return query.order_by(Setting.category, Setting.id).all()


@router.put("/", response_model=List[SettingOut])
def update_settings_bulk(
    data: SettingBulkUpdate,
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    updated = []
    for key, value in data.settings.items():
        setting = db.query(Setting).filter(Setting.key == key).first()
        if not setting:
            raise HTTPException(status_code=404, detail=f"Setting '{key}' not found")
        setting.value = value
        updated.append(setting)
    db.commit()
    for s in updated:
        db.refresh(s)
    return db.query(Setting).order_by(Setting.category, Setting.id).all()

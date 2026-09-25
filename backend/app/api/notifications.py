"""Notifications API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import DeviceToken, NotificationLog, User
from app.schemas.schemas import DeviceTokenRegister, NotificationPreferenceUpdate

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("")
def list_notification_prefs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all notification preferences."""
    prefs = (
        db.query(NotificationLog)
        .filter(NotificationLog.user_id == current_user.id)
        .order_by(NotificationLog.event_type)
        .all()
    )
    return [{"event_type": p.event_type, "is_enabled": p.is_enabled} for p in prefs]


@router.put("/{event_type}")
def update_notification_pref(
    event_type: str = Path(min_length=1, max_length=50, pattern=r"^[a-z][a-z0-9_]*$"),
    data: NotificationPreferenceUpdate = ...,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a specific notification preference."""
    pref = (
        db.query(NotificationLog)
        .filter(
            NotificationLog.user_id == current_user.id,
            NotificationLog.event_type == event_type,
        )
        .first()
    )
    if pref is None:
        pref = NotificationLog(user_id=current_user.id, event_type=event_type)

    pref.is_enabled = data.is_enabled
    db.add(pref)
    db.commit()
    return {"status": "updated"}


@router.post("/devices")
def register_device(
    token_data: DeviceTokenRegister,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Register a device token for push notifications."""
    existing = db.query(DeviceToken).filter(DeviceToken.token == token_data.token).first()
    if existing is not None and existing.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Device is already registered")

    if existing is None:
        existing = DeviceToken(user_id=current_user.id, **token_data.model_dump())
    else:
        existing.device_type = token_data.device_type
        existing.platform = token_data.platform
        existing.is_active = True
    db.add(existing)
    db.commit()
    return {"status": "registered"}


@router.delete("/devices/{device_id}")
def unregister_device(
    device_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Deactivate a device registered by the current user."""
    device = (
        db.query(DeviceToken)
        .filter(DeviceToken.id == device_id, DeviceToken.user_id == current_user.id)
        .first()
    )
    if device is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
    device.is_active = False
    db.commit()
    return {"status": "unregistered"}

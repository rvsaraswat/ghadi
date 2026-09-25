"""Preferences API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import User, UserPreference
from app.schemas.schemas import PreferencesUpdate

router = APIRouter(prefix="/user/preferences", tags=["User Preferences"])


@router.put("")
def update_preferences(
    data: PreferencesUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update user preferences (location, language, theme)."""
    if data.location is None and data.language is None and data.theme is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="At least one preference field must be supplied",
        )

    pref = (
        db.query(UserPreference)
        .filter(UserPreference.user_id == current_user.id)
        .order_by(UserPreference.id)
        .first()
    )
    if pref is None:
        pref = UserPreference(user_id=current_user.id)

    if data.location is not None:
        pref.latitude = data.location.latitude
        pref.longitude = data.location.longitude
        pref.elevation = data.location.elevation
        pref.timezone = data.location.timezone

    if data.language is not None:
        pref.language = data.language
    if data.theme is not None:
        pref.theme = data.theme

    db.add(pref)
    db.commit()
    return {"status": "updated"}

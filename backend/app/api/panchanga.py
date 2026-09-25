"""Panchanga API endpoints."""

from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import User, UserPreference
from app.schemas.schemas import PanchangaResponse
from app.services.panchanga_service import get_or_calculate_panchanga

router = APIRouter(prefix="/panchanga", tags=["Panchanga"])


@router.get("/calculate", response_model=PanchangaResponse)
def calculate_panchanga(
    db: Session = Depends(get_db),
    latitude: float = Query(default=25.3176, ge=-90, le=90),
    longitude: float = Query(default=82.9739, ge=-180, le=180),
    elevation: float = Query(default=0.0, ge=-500, le=10_000),
    timezone: str = Query(default="Asia/Kolkata", min_length=1, max_length=64),
):
    """Calculate Panchanga data for a supplied location without storing user data."""
    try:
        ZoneInfo(timezone)
    except ZoneInfoNotFoundError as exc:
        raise HTTPException(status_code=422, detail="Timezone must be a valid IANA timezone") from exc
    return PanchangaResponse(**get_or_calculate_panchanga(
        db=db, latitude=latitude, longitude=longitude,
        elevation=elevation, timezone=timezone,
    ))


@router.get("", response_model=PanchangaResponse)
def get_today_panchanga(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get today's complete Panchanga data."""
    pref = db.query(UserPreference).filter(UserPreference.user_id == current_user.id).first()
    if pref is None:
        pref = UserPreference(
        latitude=28.6139, longitude=77.209, timezone="Asia/Kolkata"
    )
    return PanchangaResponse(**get_or_calculate_panchanga(
        db, pref.latitude, pref.longitude, pref.elevation, pref.timezone
    ))

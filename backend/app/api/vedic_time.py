"""Vedic Time API endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import User, UserPreference
from app.schemas.schemas import VedicTimeResponse, SunriseSunsetResponse
from app.services.panchanga_service import get_or_calculate_panchanga

router = APIRouter(prefix="/vedic-time", tags=["Vedic Time"])


@router.get("", response_model=VedicTimeResponse)
def get_current_vedic_time(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """Get current Vedic time including Tithi, Nakshatra, Yoga, Karana."""
    pref = db.query(UserPreference).filter(UserPreference.user_id == current_user.id).first()
    pref = pref or UserPreference(latitude=28.6139, longitude=77.209, timezone="Asia/Kolkata")
    data = get_or_calculate_panchanga(db, pref.latitude, pref.longitude, pref.elevation, pref.timezone)
    return VedicTimeResponse(
        current_time=data["date"], sunrise=data["solar"]["sunrise"], sunset=data["solar"]["sunset"],
        muhurta=data.get("muhurta"), tithi_name=data["lunar"]["tithi_name"],
        nakshatra_name=data["lunar"]["nakshatra_name"], yoga_name=data["lunar"]["yoga_name"],
        karana_name=data["lunar"]["karana_name"],
    )


@router.get("/sunrise-sunset", response_model=SunriseSunsetResponse)
def get_sunrise_sunset(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """Get today's sunrise, sunset, moonrise, moonset times."""
    pref = db.query(UserPreference).filter(UserPreference.user_id == current_user.id).first()
    pref = pref or UserPreference(latitude=28.6139, longitude=77.209, timezone="Asia/Kolkata")
    data = get_or_calculate_panchanga(db, pref.latitude, pref.longitude, pref.elevation, pref.timezone)
    return SunriseSunsetResponse(date=data["date"], **data["solar"])

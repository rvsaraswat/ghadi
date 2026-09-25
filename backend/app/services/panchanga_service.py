"""Panchanga calculation service."""

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.astronomy import (
    SwissEphemeris, calculate_sunrise_sunset, 
    calculate_moonrise_moonset, calculate_tithi,
    calculate_nakshatra, calculate_yoga, calculate_karana,
    calculate_muhurta, calculate_brahma_muhurta, calculate_rahu_kaal,
)
from app.models.models import PanchangaCache


def get_today_panchanga(db: Session, latitude: float = 28.6139, longitude: float = 77.209, 
                         elevation: float = 0, timezone: str = "Asia/Kolkata") -> dict:
    """Calculate complete Panchanga for today."""
    now = datetime.now(ZoneInfo(timezone)).replace(tzinfo=None)
    
    # Get or calculate sunrise/sunset
    solar_data = calculate_sunrise_sunset(now, latitude, longitude, elevation, timezone)
    moon_data = calculate_moonrise_moonset(now, latitude, longitude, timezone)
    
    # Calculate celestial positions
    sun_pos = SwissEphemeris.calculate_sun_position(now, latitude, longitude)
    moon_pos = SwissEphemeris.calculate_moon_position(now)
    
    # Calculate Vedic time elements
    tithi = calculate_tithi(now, sun_pos["longitude"], moon_pos["longitude"])
    nakshatra = calculate_nakshatra(now, moon_pos["longitude"])
    yoga = calculate_yoga(now, sun_pos["longitude"], moon_pos["longitude"])
    karana = calculate_karana(now)
    
    # Calculate time windows
    sunrise = solar_data.get("sunrise") or now.replace(hour=6, minute=0)
    sunset = solar_data.get("sunset") or now.replace(hour=18, minute=0)
    
    brahma = calculate_brahma_muhurta(now, sunrise)
    rahu = calculate_rahu_kaal(now, sunrise)
    
    # Current muhurta
    current_muhurta = calculate_muhurta(now, sunrise, sunset)
    
    return {
        "date": now,
        "latitude": latitude,
        "longitude": longitude,
        "timezone": timezone,
        "solar": {
            "sunrise": solar_data.get("sunrise"),
            "sunset": solar_data.get("sunset"),
            "noon": solar_data.get("noon"),
            "moonrise": moon_data.get("moonrise"),
            "moonset": moon_data.get("moonset"),
        },
        "lunar": {
            "tithi_name": tithi["name"],
            "paksha": tithi["paksha"],
            "nakshatra_name": nakshatra["name"],
            "yoga_name": yoga["name"],
            "karana_name": karana["name"],
        },
        "time_windows": {
            "brahma_muhurta_start": brahma.get("start"),
            "abhijit_muhurta_start": sunrise + timedelta(minutes=48),  # Middle 48 min of day
            "rahu_kaal_start": rahu.get("start"),
            "rahu_kaal_end": rahu.get("end"),
        },
        "muhurta": current_muhurta,
    }


def cache_panchanga(db: Session, panchanga_data: dict) -> PanchangaCache:
    """Cache today's Panchanga data in database."""
    date = panchanga_data["date"].replace(hour=0, minute=0, second=0, microsecond=0)
    latitude = panchanga_data["latitude"]
    longitude = panchanga_data["longitude"]
    timezone = panchanga_data["timezone"]
    cache = db.query(PanchangaCache).filter_by(
        date=date, latitude=latitude, longitude=longitude, timezone=timezone
    ).first() or PanchangaCache(date=date, latitude=latitude, longitude=longitude, timezone=timezone)
    
    # Copy fields from calculation result
    solar = panchanga_data.get("solar", {})
    lunar = panchanga_data.get("lunar", {})
    windows = panchanga_data.get("time_windows", {})
    
    cache.sunrise_time = solar.get("sunrise")
    cache.sunset_time = solar.get("sunset")
    cache.noon_time = solar.get("noon")
    cache.moonrise_time = solar.get("moonrise")
    cache.moonset_time = solar.get("moonset")
    
    cache.tithi_name = lunar.get("tithi_name")
    cache.paksha = lunar.get("paksha")
    cache.nakshatra_name = lunar.get("nakshatra_name")
    cache.yoga_name = lunar.get("yoga_name")
    cache.karana_name = lunar.get("karana_name")
    
    cache.brahma_muhurta_start = windows.get("brahma_muhurta_start")
    cache.abhijit_muhurta_start = windows.get("abhijit_muhurta_start")
    cache.rahu_kaal_start = windows.get("rahu_kaal_start")
    cache.rahu_kaal_end = windows.get("rahu_kaal_end")
    
    db.add(cache)
    try:
        db.commit()
    except IntegrityError:
        # Another request populated the same unique daily cache key first.
        db.rollback()
        cache = db.query(PanchangaCache).filter_by(
            date=date, latitude=latitude, longitude=longitude, timezone=timezone
        ).first()
        if cache is None:
            raise
    db.refresh(cache)
    
    return cache


def cache_to_panchanga(cache: PanchangaCache) -> dict:
    """Convert a cached database row to the API calculation shape."""
    return {
        "date": cache.date,
        "latitude": cache.latitude,
        "longitude": cache.longitude,
        "timezone": cache.timezone,
        "solar": {
            "sunrise": cache.sunrise_time, "sunset": cache.sunset_time,
            "noon": cache.noon_time, "moonrise": cache.moonrise_time, "moonset": cache.moonset_time,
        },
        "lunar": {
            "tithi_name": cache.tithi_name, "paksha": cache.paksha,
            "nakshatra_name": cache.nakshatra_name, "yoga_name": cache.yoga_name,
            "karana_name": cache.karana_name,
        },
        "time_windows": {
            "brahma_muhurta_start": cache.brahma_muhurta_start,
            "abhijit_muhurta_start": cache.abhijit_muhurta_start,
            "rahu_kaal_start": cache.rahu_kaal_start, "rahu_kaal_end": cache.rahu_kaal_end,
            "yamaganda_start": cache.yamaganda_start, "yamaganda_end": cache.yamaganda_end,
            "gulika_start": cache.gulika_start, "gulika_end": cache.gulika_end,
        },
        "muhurta": cache.muhurta_count,
    }


def get_or_calculate_panchanga(db: Session, latitude: float, longitude: float, elevation: float, timezone: str) -> dict:
    """Return a location-specific daily calculation, using the database cache when available."""
    local_day = datetime.now(ZoneInfo(timezone)).replace(tzinfo=None, hour=0, minute=0, second=0, microsecond=0)
    cache = db.query(PanchangaCache).filter_by(
        date=local_day, latitude=latitude, longitude=longitude, timezone=timezone
    ).first()
    if cache is not None:
        return cache_to_panchanga(cache)
    data = get_today_panchanga(db, latitude, longitude, elevation, timezone)
    cache = cache_panchanga(db, data)
    return cache_to_panchanga(cache)

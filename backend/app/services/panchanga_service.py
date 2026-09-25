"""Panchanga calculation service."""

from datetime import datetime, timedelta
import math
from zoneinfo import ZoneInfo
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.astronomy import (
    J2000, SwissEphemeris, calculate_sunrise_sunset,
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


def get_cosmic_panchanga(at: datetime, ayanamsha_degrees: float = 27.0) -> dict:
    """Return traceable sidereal positions for the Cosmos dashboard.

    The provider boundary is intentionally kept here: this mean-orbit provider can
    be replaced by pysweph without changing the API or the visualization layer.
    """
    from app.core.astronomy import calculate_karana, calculate_nakshatra, calculate_tithi, calculate_yoga

    sun = SwissEphemeris.calculate_sun_position(at)["longitude"]
    moon = SwissEphemeris.calculate_moon_position(at)["longitude"]
    tithi = calculate_tithi(at, sun, moon)
    nakshatra = calculate_nakshatra(at, moon)
    yoga = calculate_yoga(at, sun, moon)
    karana = calculate_karana(at, sun, moon)

    rashi_names = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    nakshatra_names = ["Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"]
    days = SwissEphemeris.julian_date(at) - J2000
    orbitals = [
        ("Sun", "☉", sun, 0.985647, 0.0), ("Moon", "☽", moon, 13.176396, 0.0),
        ("Mars", "♂", 355.45 + days * 0.524020, 0.524020, 0.3),
        ("Mercury", "☿", 252.25 + days * 4.092334, 1.383, 0.1),
        ("Jupiter", "♃", 34.35 + days * 0.083056, 0.083056, 0.05),
        ("Venus", "♀", 181.98 + days * 1.602130, 1.2, 0.15),
        ("Saturn", "♄", 50.08 + days * 0.033497, 0.033497, 0.02),
        ("Rahu", "☊", 125.04 - days * 0.0529538, -0.0529538, 0.0),
        ("Ketu", "☋", 305.04 - days * 0.0529538, -0.0529538, 0.0),
    ]
    planets = []
    for name, symbol, tropical, speed, latitude in orbitals:
        longitude = (tropical - ayanamsha_degrees) % 360
        segment = longitude / (360 / 27)
        planets.append({
            "name": name, "symbol": symbol, "longitude": round(longitude, 3),
            "latitude": latitude, "rashi": rashi_names[int(longitude // 30)],
            "nakshatra": nakshatra_names[int(segment) % 27], "pada": int((segment % 1) * 4) + 1,
            "speed": round(speed, 3), "retrograde": speed < 0,
        })
    return {
        "date": at, "ayanamsha": "Lahiri", "ayanamsha_degrees": ayanamsha_degrees,
        "sun_longitude": round((sun - ayanamsha_degrees) % 360, 3),
        "moon_longitude": round((moon - ayanamsha_degrees) % 360, 3),
        "elongation": round(tithi["elongation"], 3), "tithi_number": tithi["tithi_number"],
        "tithi_name": tithi["name"], "paksha": tithi["paksha"], "nakshatra_name": nakshatra["name"],
        "yoga_name": yoga["name"], "karana_name": karana["name"], "planets": planets,
    }

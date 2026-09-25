"""Festival engine for calculating and managing festivals."""

from datetime import datetime, timedelta
from typing import List


def get_recurring_festivals(year: int = None) -> list[dict]:
    """Return a list of festivals for *year*.

    The function now calculates lunar‑based festivals (e.g., Diwali, Holi) and
    solar‑based festivals (e.g., Makar Sankranti) on the fly using the
    simplified Swiss‑Ephemeris logic in :mod:`backend.app.core.astronomy`.
    Fixed national observances are appended unchanged.
    """
    if year is None:
        year = datetime.now().year

    # Imports already available at module level; no need to import again here.

    # Helper: month names in Vedic calendar (start with Chaitra).
    month_names = [
        "Chaitra",
        "Vaishakha",
        "Jyeshtha",
        "Ashadha",
        "Shravana",
        "Bhadrapada",
        "Ashwin",
        "Kartika",
        "Margashirsha",
        "Pausha",
        "Magha",
        "Phalguna",
    ]

    # Build a daily table for the whole year.
    start = datetime(year, 1, 1)
    days = [start + timedelta(days=i) for i in range(366) if start + timedelta(days=i) < datetime(year + 1, 1, 1)]
    month_index = -1
    current_month = None
    festivals = []
    sakranti_recorded = False

    for dt in days:
        sun_pos = SwissEphemeris.calculate_sun_position(dt)
        moon_pos = SwissEphemeris.calculate_moon_position(dt)
        tithi = calculate_tithi(dt, sun_pos["longitude"], moon_pos["longitude"])

        # Detect start of new lunar month: tithi 1 of Shukla paksha.
        if tithi["tithi_number"] == 1 and tithi["paksha"] == "Shukla":
            month_index = (month_index + 1) % 12
            current_month = month_names[month_index]

        # Solar festival: Makar Sankranti (sun enters Capricorn, 300°-330°).
        if not sakranti_recorded and sun_pos["longitude"] >= 300:
            festivals.append(
                {
                    "name": "Makar Sankranti",
                    "date": dt.strftime("%Y-%m-%d"),
                    "significance": "Sun enters Capricorn",
                    "type": "solar",
                }
            )
            sakranti_recorded = True

        # Lunar festivals based on tithi and month.
        if tithi["name"] == "Amavasya" and tithi["paksha"] == "Krishna":
            if current_month == "Kartika":
                festivals.append(
                    {
                        "name": "Diwali",
                        "date": dt.strftime("%Y-%m-%d"),
                        "significance": "Festival of lights on Kartika Amavasya",
                        "type": "lunar",
                    }
                )
            elif current_month == "Phalguna":
                festivals.append(
                    {
                        "name": "Holi",
                        "date": dt.strftime("%Y-%m-%d"),
                        "significance": "Festival of colors on Phalguna Amavasya",
                        "type": "lunar",
                    }
                )

        if tithi["name"] == "Panchami" and tithi["paksha"] == "Shukla" and current_month == "Vaishakha":
            festivals.append(
                {
                    "name": "Vasant Panchami",
                    "date": dt.strftime("%Y-%m-%d"),
                    "significance": "Spring festival honoring Saraswati",
                    "type": "lunar",
                }
            )

    # Append fixed national dates.
    fixed = [
        {"name": "Republic Day", "date": f"{year}-01-26", "significance": "National observance", "type": "national"},
        {"name": "Independence Day", "date": f"{year}-08-15", "significance": "National observance", "type": "national"},
        {"name": "Christmas", "date": f"{year}-12-25", "significance": "Christian observance", "type": "national"},
    ]
    festivals.extend(fixed)

    # Sort by date for consistency.
    festivals.sort(key=lambda f: f["date"])
    return festivals


def get_festival_countdown(festival_date_str: str, now: datetime = None) -> dict:
    """Calculate countdown to a festival."""
    now = now or datetime.utcnow()
    
    try:
        from dateutil import parser as date_parser
        festival_date = date_parser.parse(festival_date_str)
    except ImportError:
        # Fallback if python-dateutil not available
        festival_date = datetime.strptime(festival_date_str[:10], "%Y-%m-%d")
    
    delta = (festival_date - now).days
    
    return {
        "festival_date": festival_date,
        "days_until": max(0, delta),
        "is_today": delta <= 0 and delta > -1,
        "has_passed": delta < 0,
    }

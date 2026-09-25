"""Festival engine for calculating and managing festivals."""

from datetime import datetime, timedelta
from typing import List


def get_recurring_festivals(year: int = None) -> list[dict]:
    """Get all recurring festivals for a given year (lunar calendar based)."""
    
    if year is None:
        year = datetime.now().year
    
    # Pan-Indian observances. Lunar observances vary by sampradaya and location;
    # production catalog updates should be sourced from a verified Panchanga provider.
    return [
        {"name": "Makar Sankranti", "date": f"{year}-01-14", "significance": "Sun enters Capricorn", "type": "solar"},
        {"name": "Republic Day", "date": f"{year}-01-26", "significance": "National observance", "type": "national"},
        {"name": "Vasant Panchami", "date": f"{year}-02-03", "significance": "Spring festival honoring Saraswati", "type": "lunar"},
        {"name": "Thaipusam", "date": f"{year}-02-11", "significance": "Murugan observance", "type": "lunar"},
        {"name": "Holi", "date": f"{year}-03-14", "significance": "Festival of colors", "type": "lunar"},
        {"name": "Ram Navami", "date": f"{year}-04-17", "significance": "Birth of Lord Rama", "type": "lunar"},
        {"name": "Vaisakhi", "date": f"{year}-04-14", "significance": "Harvest and Sikh new year observance", "type": "solar"},
        {"name": "Buddha Purnima", "date": f"{year}-05-12", "significance": "Birth, enlightenment, and parinirvana of Buddha", "type": "lunar"},
        {"name": "Rath Yatra", "date": f"{year}-06-27", "significance": "Jagannath chariot festival", "type": "lunar"},
        {"name": "Guru Purnima", "date": f"{year}-07-10", "significance": "Honoring teachers and gurus", "type": "lunar"},
        {"name": "Independence Day", "date": f"{year}-08-15", "significance": "National observance", "type": "national"},
        {"name": "Raksha Bandhan", "date": f"{year}-08-17", "significance": "Celebration between siblings", "type": "lunar"},
        {"name": "Onam", "date": f"{year}-09-05", "significance": "Kerala harvest festival", "type": "regional"},
        {"name": "Ganesh Chaturthi", "date": f"{year}-09-10", "significance": "Birth of Lord Ganesha", "type": "lunar"},
        {"name": "Navratri begins", "date": f"{year}-10-02", "significance": "Nine nights of divine worship", "type": "lunar"},
        {"name": "Dussehra", "date": f"{year}-10-12", "significance": "Victory of good over evil", "type": "lunar"},
        {"name": "Gandhi Jayanti", "date": f"{year}-10-02", "significance": "National observance", "type": "national"},
        {"name": "Diwali", "date": f"{year}-11-01", "significance": "Festival of lights", "type": "lunar"},
        {"name": "Guru Nanak Jayanti", "date": f"{year}-11-15", "significance": "Birth of Guru Nanak Dev Ji", "type": "lunar"},
        {"name": "Christmas", "date": f"{year}-12-25", "significance": "Christian observance", "type": "national"},
        {"name": "Maha Shivaratri", "date": f"{year}-02-26", "significance": "Night of Lord Shiva", "type": "lunar"},
        {"name": "Janmashtami", "date": f"{year}-08-26", "significance": "Birth of Lord Krishna", "type": "lunar"},
    ]


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

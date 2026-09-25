"""SQLAlchemy database models."""

from datetime import datetime, timezone
from sqlalchemy import (
    Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    """User model for authentication and personalization."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    preferences = relationship("UserPreference", back_populates="user", uselist=False, cascade="all, delete-orphan")
    notifications = relationship("NotificationLog", back_populates="user")
    device_tokens = relationship("DeviceToken", back_populates="user", cascade="all, delete-orphan")


class UserPreference(Base):
    """User preferences for location and settings."""
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    latitude = Column(Float, default=28.6139)  # Default: Delhi
    longitude = Column(Float, default=77.209)
    elevation = Column(Float, default=0)
    timezone = Column(String(50), default="Asia/Kolkata")
    language = Column(String(10), default="en")
    theme = Column(String(10), default="light")
    is_premium = Column(Boolean, default=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="preferences")


class Location(Base):
    """Stored locations for multi-location support."""
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    elevation = Column(Float, default=0)
    timezone = Column(String(50))
    is_primary = Column(Boolean, default=True)

    __table_args__ = (UniqueConstraint("user_id", "name", name="uq_user_location_name"),)


class Festival(Base):
    """Festival definitions and occurrences."""
    __tablename__ = "festivals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    date = Column(DateTime, nullable=False, index=True)
    is_recurring = Column(Boolean, default=True)
    recurrence_pattern = Column(Text)  # JSON pattern for recurring festivals
    significance = Column(Text)
    observance_details = Column(Text)
    regional_variations = Column(Text)  # JSON: region -> name mapping

    __table_args__ = (UniqueConstraint("name", "date", name="uq_festival_name_date"),)


class PanchangaCache(Base):
    """Cached daily Vedic time calculations for offline mode."""
    __tablename__ = "panchanga_cache"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    timezone = Column(String(50))
    sunrise_time = Column(DateTime)
    sunset_time = Column(DateTime)
    noon_time = Column(DateTime)
    moonrise_time = Column(DateTime)
    moonset_time = Column(DateTime)
    tithi_name = Column(String(100))
    tithi_end = Column(DateTime)
    paksha = Column(String(20))  # Shukla or Krishna
    nakshatra_name = Column(String(100))
    nakshatra_end = Column(DateTime)
    yoga_name = Column(String(100))
    yoga_end = Column(DateTime)
    karana_name = Column(String(100))
    karana_end = Column(DateTime)
    brahma_muhurta_start = Column(DateTime)
    abhijit_muhurta_start = Column(DateTime)
    rahu_kaal_start = Column(DateTime)
    rahu_kaal_end = Column(DateTime)
    yamaganda_start = Column(DateTime)
    yamaganda_end = Column(DateTime)
    gulika_start = Column(DateTime)
    gulika_end = Column(DateTime)
    muhurta_count = Column(Integer, default=0)
    data_json = Column(Text)  # Full JSON data for backup

    __table_args__ = (UniqueConstraint("date", "latitude", "longitude", "timezone", name="uq_panchanga_date_location_timezone"),)


class NotificationLog(Base):
    """Notification preferences and delivery tracking."""
    __tablename__ = "notification_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    event_type = Column(String(50), nullable=False)  # brahma_muhurta, festival, ekadashi, etc.
    is_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    user = relationship("User", back_populates="notifications")

    __table_args__ = (UniqueConstraint("user_id", "event_type", name="uq_notification_user_event"),)


class DeviceToken(Base):
    """Device tokens for push notifications."""
    __tablename__ = "device_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    device_type = Column(String(20), nullable=False)  # ios, android, web, watch
    token = Column(String(500), nullable=False, unique=True, index=True)
    platform = Column(String(20), nullable=False)  # apns, fcm
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    user = relationship("User", back_populates="device_tokens")

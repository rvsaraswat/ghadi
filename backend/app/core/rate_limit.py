"""Rate limiting configuration."""

from slowapi import Limiter
from slowapi.util import get_remote_address

from app.config import settings


storage_uri = settings.REDIS_URL if settings.ENVIRONMENT == "production" else "memory://"
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[f"{settings.RATE_LIMIT_PER_MINUTE}/minute"],
    storage_uri=storage_uri,
)
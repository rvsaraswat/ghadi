"""API route dependencies."""

from fastapi import Depends

from app.core.security import get_current_user
from app.models.models import User


def require_auth(current_user: User = Depends(get_current_user)) -> User:
    """Require the shared, validated current-user dependency."""
    return current_user

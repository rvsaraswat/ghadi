"""Security utilities for authentication and password hashing."""

from datetime import datetime, timedelta, timezone
from typing import Any, Mapping
from uuid import uuid4

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.config import settings
from app.core.database import get_db
from app.models.models import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def _credentials_exception() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def _jwt_secret() -> str:
    if not settings.SECRET_KEY or len(settings.SECRET_KEY) < 32:
        raise RuntimeError("SECRET_KEY must be configured with at least 32 characters")
    return settings.SECRET_KEY


def password_policy_errors(password: str) -> list[str]:
    """Return human-readable password policy violations for registration flows."""
    errors: list[str] = []
    if len(password) < settings.MIN_PASSWORD_LENGTH:
        errors.append(f"Password must be at least {settings.MIN_PASSWORD_LENGTH} characters long")
    if len(password.encode("utf-8")) > 72:
        errors.append("Password must not exceed 72 UTF-8 bytes")
    if not any(character.islower() for character in password):
        errors.append("Password must include a lowercase letter")
    if not any(character.isupper() for character in password):
        errors.append("Password must include an uppercase letter")
    if not any(character.isdigit() for character in password):
        errors.append("Password must include a number")
    if not any(not character.isalnum() for character in password):
        errors.append("Password must include a symbol")
    return errors


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except (TypeError, ValueError):
        return False


def create_access_token(data: Mapping[str, Any], expires_delta: timedelta | None = None) -> str:
    """Create a JWT access token."""
    subject = data.get("sub")
    if not isinstance(subject, str) or not subject:
        raise ValueError("Token data must include a non-empty subject")

    now = datetime.now(timezone.utc)
    expires_at = now + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = dict(data)
    to_encode.update({"exp": expires_at, "iat": now, "nbf": now, "jti": str(uuid4())})
    return jwt.encode(to_encode, _jwt_secret(), algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    """Decode and validate a JWT access token."""
    try:
        payload = jwt.decode(
            token,
            _jwt_secret(),
            algorithms=[settings.JWT_ALGORITHM],
            options={"require_exp": True},
        )
    except JWTError as exc:
        raise _credentials_exception() from exc

    if not isinstance(payload.get("sub"), str) or not payload["sub"]:
        raise _credentials_exception()
    return payload


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """Get the current authenticated user from JWT token."""
    payload = decode_access_token(token)
    email = payload.get("sub")
    user = db.query(User).filter(User.email == email).first()
    if not user or not user.is_active:
        raise _credentials_exception()
    return user

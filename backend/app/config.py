"""Application configuration."""

from typing import Annotated, Literal

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables or .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )

    # Application
    APP_NAME: str = "Aarohanam"
    ENVIRONMENT: Literal["development", "test", "staging", "production"] = "development"
    DEBUG: bool = False
    SECRET_KEY: str | None = None
    JWT_ALGORITHM: Literal["HS256"] = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60 * 24, ge=5, le=60 * 24 * 30)
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    TRUSTED_HOSTS: Annotated[list[str], NoDecode] = Field(default_factory=list)
    FRONTEND_ORIGINS: Annotated[list[str], NoDecode] = Field(default_factory=list)
    REQUEST_MAX_BODY_SIZE: int = Field(default=1_048_576, ge=1_024, le=10_485_760)

    # Database — defaults to local SQLite so the app runs with zero setup.
    # Override with e.g. postgresql://user:pass@host:5432/vedic_time in .env
    DATABASE_URL: str = "sqlite:///./vedic_clock.db"
    DB_POOL_SIZE: int = Field(default=5, ge=1, le=100)
    DB_MAX_OVERFLOW: int = Field(default=10, ge=0, le=100)

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # API Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = Field(default=60, ge=1, le=10_000)
    MIN_PASSWORD_LENGTH: int = Field(default=12, ge=8, le=128)

    @field_validator("TRUSTED_HOSTS", "FRONTEND_ORIGINS", mode="before")
    @classmethod
    def parse_comma_separated_list(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, list):
            return value
        return [item.strip().rstrip("/") for item in value.split(",") if item.strip()]

    @model_validator(mode="after")
    def validate_production_settings(self) -> "Settings":
        if self.ENVIRONMENT != "production":
            return self

        if self.DEBUG:
            raise ValueError("DEBUG must be disabled in production")
        if not self.SECRET_KEY or len(self.SECRET_KEY) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters in production")
        if not self.DATABASE_URL.startswith(("postgresql://", "postgresql+psycopg2://")):
            raise ValueError("DATABASE_URL must use PostgreSQL in production")
        if not self.FRONTEND_ORIGINS:
            raise ValueError("FRONTEND_ORIGINS must contain at least one explicit origin in production")
        if "*" in self.FRONTEND_ORIGINS:
            raise ValueError("FRONTEND_ORIGINS cannot contain a wildcard in production")
        if not self.TRUSTED_HOSTS or "*" in self.TRUSTED_HOSTS:
            raise ValueError("TRUSTED_HOSTS must contain explicit hosts in production")
        return self


settings = Settings()

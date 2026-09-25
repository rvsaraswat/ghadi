"""Aarohanam Vedic Time Companion - FastAPI Backend."""

import logging
import time
from contextlib import asynccontextmanager
from pathlib import Path
from uuid import UUID, uuid4

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy import text
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.staticfiles import StaticFiles

from app.api import auth, vedic_time, panchanga, festivals, preferences, notifications
from app.core.database import Base, engine
from app.core.logging import configure_logging, reset_request_id, set_request_id
from app.core.rate_limit import limiter
from app.config import settings


logger = logging.getLogger(__name__)
web_root = Path(__file__).resolve().parent / "web"


def _request_id_from_header(request: Request) -> str:
    """Accept a well-formed correlation ID or create a new one."""
    candidate = request.headers.get("X-Request-ID")
    if candidate:
        try:
            return str(UUID(candidate))
        except ValueError:
            pass
    return str(uuid4())


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Configure process services and retain local development convenience."""
    configure_logging(settings.LOG_LEVEL)
    logger.info("application_starting", extra={"environment": settings.ENVIRONMENT})
    if settings.ENVIRONMENT == "development":
        Base.metadata.create_all(bind=engine)
    yield
    logger.info("application_stopped")


app = FastAPI(
    title="Aarohanam API",
    description="Vedic Time Companion - Ayan OS Backend",
    version="1.0.0",
    lifespan=lifespan,
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.FRONTEND_ORIGINS,
    allow_credentials=bool(settings.FRONTEND_ORIGINS),
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
    expose_headers=["X-Request-ID"],
)

if settings.TRUSTED_HOSTS:
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.TRUSTED_HOSTS)


@app.middleware("http")
async def add_request_context(request: Request, call_next):
    """Correlate request logs and publish the correlation ID to clients."""
    request_id = _request_id_from_header(request)
    request.state.request_id = request_id
    context_token = set_request_id(request_id)
    started_at = time.perf_counter()
    try:
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        logger.info(
            "request_completed",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": round((time.perf_counter() - started_at) * 1000, 2),
            },
        )
        return response
    finally:
        reset_request_id(context_token)


@app.exception_handler(RequestValidationError)
async def handle_validation_error(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Return safe validation details without echoing submitted values."""
    details = [
        {"location": list(error["loc"]), "message": error["msg"], "type": error["type"]}
        for error in exc.errors()
    ]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        headers={"X-Request-ID": request.state.request_id},
        content={
            "error": {
                "code": "validation_error",
                "message": "Request validation failed",
                "details": details,
                "request_id": request.state.request_id,
            }
        },
    )


@app.exception_handler(Exception)
async def handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
    """Log internal faults without exposing implementation details to clients."""
    logger.exception("unhandled_exception", exc_info=exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        headers={"X-Request-ID": request.state.request_id},
        content={
            "error": {
                "code": "internal_server_error",
                "message": "An unexpected error occurred",
                "request_id": request.state.request_id,
            }
        },
    )


@app.get("/health/live", tags=["Health"])
def liveness() -> dict[str, str]:
    """Report whether the API process is accepting requests."""
    return {"status": "ok"}


@app.get("/health/ready", tags=["Health"])
def readiness() -> JSONResponse:
    """Report whether essential backing services are reachable."""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except Exception:
        logger.exception("readiness_check_failed")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "unavailable"},
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content={"status": "ok"})


app.mount("/assets", StaticFiles(directory=web_root), name="assets")


@app.get("/", include_in_schema=False)
def dashboard() -> FileResponse:
    """Serve the browser dashboard."""
    return FileResponse(web_root / "index.html")


app.include_router(auth.router)
app.include_router(vedic_time.router)
app.include_router(panchanga.router)
app.include_router(festivals.router)
app.include_router(preferences.router)
app.include_router(notifications.router)

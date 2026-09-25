"""Structured logging and request correlation helpers."""

import json
import logging
import sys
from contextvars import ContextVar, Token
from datetime import datetime, timezone
from typing import Any


request_id_context: ContextVar[str | None] = ContextVar("request_id", default=None)
_BUILTIN_LOG_RECORD_FIELDS = frozenset(logging.makeLogRecord({}).__dict__)


class JsonFormatter(logging.Formatter):
    """Render log records as newline-delimited JSON for container platforms."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        request_id = request_id_context.get()
        if request_id:
            payload["request_id"] = request_id
        payload.update(
            {
                key: value
                for key, value in record.__dict__.items()
                if key not in _BUILTIN_LOG_RECORD_FIELDS and not key.startswith("_")
            }
        )
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, default=str, ensure_ascii=True)


def configure_logging(log_level: str) -> None:
    """Configure a single structured handler without duplicating handlers."""
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    for handler in root_logger.handlers:
        if handler.get_name() == "aarohanam-json":
            handler.setLevel(log_level)
            return

    handler = logging.StreamHandler(sys.stdout)
    handler.set_name("aarohanam-json")
    handler.setLevel(log_level)
    handler.setFormatter(JsonFormatter())
    root_logger.addHandler(handler)


def set_request_id(request_id: str) -> Token[str | None]:
    """Store a request identifier for logs emitted in the current context."""
    return request_id_context.set(request_id)


def reset_request_id(token: Token[str | None]) -> None:
    """Clear request correlation after a request has completed."""
    request_id_context.reset(token)
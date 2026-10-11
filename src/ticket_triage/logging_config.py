"""JSON logging and request correlation context."""

import json
import logging
import re
from contextvars import ContextVar
from datetime import UTC, datetime
from logging.config import dictConfig
from typing import Any

correlation_id_var: ContextVar[str] = ContextVar(
    "correlation_id",
    default="-",
)

# Accept only simple, bounded IDs from upstream callers.
_CORRELATION_ID_PATTERN = re.compile(r"^[A-Za-z0-9._-]{1,100}$")


def valid_correlation_id(value: str | None) -> bool:
    return bool(value and _CORRELATION_ID_PATTERN.fullmatch(value))


class JsonFormatter(logging.Formatter):
    """Serialize log records as one JSON object per line."""

    RESERVED = set(logging.makeLogRecord({}).__dict__.keys()) | {"message", "asctime"}

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "correlation_id": correlation_id_var.get(),
        }

        # Add explicitly supplied structured fields.
        for key, value in record.__dict__.items():
            if key not in self.RESERVED and not key.startswith("_"):
                payload[key] = value

        if record.exc_info:
            # Exception messages can contain sensitive information.
            # Prefer exception type and a controlled event description.
            payload["exception_type"] = (
                record.exc_info[0].__name__ if record.exc_info[0] else "Exception"
            )

        return json.dumps(payload, default=str, ensure_ascii=False)


def configure_logging(level: str = "INFO") -> None:
    """Configure root logging once during application startup."""
    normalized_level = level.upper()
    if normalized_level not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
        raise ValueError("Unsupported logging level.")

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "json",
                }
            },
            "formatters": {
                "json": {"()": "ticket_triage.logging_config.JsonFormatter"}
            },
            "root": {
                "handlers": ["console"],
                "level": normalized_level,
            },
        }
    )

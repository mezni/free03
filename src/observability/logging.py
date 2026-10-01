import json
import logging
import sys
from typing import Any

from src.observability.context import get_request_id

_STRUCTURED_FIELDS = (
    "event",
    "duration_ms",
    "model",
    "retrieved_count",
    "prompt_tokens",
    "completion_tokens",
    "total_tokens",
    "status_code",
    "path",
    "method",
    "error_type",
)


class JsonFormatter(logging.Formatter):

    def format(
        self,
        record: logging.LogRecord,
    ) -> str:
        payload: dict[str, Any] = {
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        request_id = get_request_id()

        if request_id is not None:
            payload["request_id"] = request_id

        for field in _STRUCTURED_FIELDS:
            if hasattr(record, field):
                payload[field] = getattr(record, field)

        if record.exc_info is not None:
            payload["exception"] = self.formatException(
                record.exc_info
            )

        return json.dumps(payload, default=str)


def configure_logging(
    level: str = "INFO",
) -> None:
    handler = logging.StreamHandler(sys.stdout)

    handler.setFormatter(JsonFormatter())

    root_logger = logging.getLogger()

    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(level)
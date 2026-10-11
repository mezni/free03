import time
from collections.abc import Callable
from typing import TypeVar

from ticket_triage.metrics import (
    CLASSIFICATION_DURATION,
    CLASSIFICATION_ATTEMPTS,
)

T = TypeVar("T")


def observe_classification(operation: Callable[[], T]) -> T:
    started_at = time.monotonic()

    try:
        result = operation()
    except Exception:
        CLASSIFICATION_ATTEMPTS.labels(outcome="failure").inc()
        raise
    else:
        CLASSIFICATION_ATTEMPTS.labels(outcome="success").inc()
        return result
    finally:
        CLASSIFICATION_DURATION.observe(time.monotonic() - started_at)
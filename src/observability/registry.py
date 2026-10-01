from threading import Lock

from src.observability.metrics import MetricsCollector

_metrics: MetricsCollector | None = None
_metrics_lock = Lock()


def get_metrics() -> MetricsCollector:
    """Return the process-wide collector.

    A single collector must be shared across every
    `ApplicationContainer`. The API builds a new container per request
    via `get_rag_service`, so a collector created inside the container
    constructor would reset on each request and `/metrics` would only
    ever report the in-flight request.
    """
    global _metrics

    if _metrics is None:
        with _metrics_lock:
            if _metrics is None:
                _metrics = MetricsCollector()

    return _metrics


def set_metrics(
    collector: MetricsCollector,
) -> None:
    """Replace the process-wide collector (used by tests)."""
    global _metrics

    with _metrics_lock:
        _metrics = collector


def reset_metrics() -> None:
    set_metrics(MetricsCollector())

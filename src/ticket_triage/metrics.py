"""Low-overhead Prometheus metrics for ticket triage."""

from prometheus_client import (
    CONTENT_TYPE_LATEST,
    REGISTRY,
    Counter,
    Histogram,
    generate_latest,
)

HTTP_REQUESTS = Counter(
    "ticket_triage_http_requests_total",
    "Total HTTP requests handled by the API.",
    ["method", "status"],
)

HTTP_REQUEST_DURATION = Histogram(
    "ticket_triage_http_request_duration_seconds",
    "HTTP request duration in seconds.",
    ["method"],
)

CLASSIFICATION_ATTEMPTS = Counter(
    "ticket_triage_classification_attempts_total",
    "Classification attempts by outcome.",
    ["outcome"],
)

CLASSIFICATION_DURATION = Histogram(
    "ticket_triage_classification_duration_seconds",
    "Classification duration in seconds.",
)


def render_metrics() -> tuple[bytes, str]:
    """Render process metrics in Prometheus exposition format."""
    return generate_latest(REGISTRY), CONTENT_TYPE_LATEST

from prometheus_client import Counter, Gauge, Histogram


# --- HTTP metrics ---

HTTP_REQUESTS = Counter(
    "triage_http_requests_total",
    "Total number of HTTP requests",
    ["method", "status"],
)

HTTP_REQUEST_DURATION = Histogram(
    "triage_http_request_duration_seconds",
    "HTTP request duration in seconds",
    buckets=(0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10, 30),
    labelnames=["method"],
)

# --- Classification metrics ---

CLASSIFICATION_ATTEMPTS = Counter(
    "triage_classification_attempts_total",
    "Classification attempts by final outcome",
    ["outcome"],
)

CLASSIFICATION_DURATION = Histogram(
    "triage_classification_duration_seconds",
    "Time spent classifying a ticket",
    buckets=(0.1, 0.25, 0.5, 1, 2, 5, 10, 20, 30),
)

# --- LLM provider metrics ---

LLM_RETRIES = Counter(
    "triage_llm_retries_total",
    "LLM retries by error category",
    ["error_type"],
)

LLM_TIMEOUTS = Counter(
    "triage_llm_timeouts_total",
    "LLM request timeouts",
)

# --- Rate limiter metrics ---

RATE_LIMIT_REJECTIONS = Counter(
    "triage_rate_limit_rejections_total",
    "Requests rejected by local rate limiting",
)

# --- Queue metrics ---

QUEUE_JOBS = Gauge(
    "triage_queue_jobs",
    "Current jobs by queue status",
    ["status"],
)

# --- Routing metrics ---

ROUTING_OUTCOMES = Counter(
    "triage_routing_outcomes_total",
    "Routing operation outcomes",
    ["outcome"],
)

# --- Circuit breaker metrics ---

CIRCUIT_BREAKER_REJECTIONS = Counter(
    "triage_circuit_breaker_rejections_total",
    "Requests rejected because the circuit is open",
)


def render_metrics():
    """Return Prometheus exposition-format metrics payload and content type."""
    from prometheus_client import generate_latest

    content = generate_latest()
    return content, "text/plain; version=1.0.0; charset=utf-8"
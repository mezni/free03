"""Which HTTP failures are worth retrying.

Classification is kept apart from the retry mechanism on purpose. The
retry policy decides *how long to wait*; this module decides *whether a
failure could ever succeed later*. Conflating the two makes it easy to
end up retrying a 400 until the process gives up, which adds load
without ever changing the outcome.
"""

# Transient server-side and throttling responses. A 400/401/404/422 is
# excluded deliberately: those are deterministic rejections that will
# fail identically on every attempt.
RETRYABLE_STATUS_CODES: frozenset[int] = frozenset(
    {
        408,
        429,
        500,
        502,
        503,
        504,
    }
)

# Statuses that a client must fix before a retry could succeed.
NON_RETRYABLE_STATUS_CODES: frozenset[int] = frozenset(
    {
        400,
        401,
        403,
        404,
        405,
        409,
        413,
        422,
    }
)


def is_retryable_status(status_code: int) -> bool:
    """Return whether an HTTP status may succeed on a later attempt."""
    if status_code in NON_RETRYABLE_STATUS_CODES:
        return False

    return status_code in RETRYABLE_STATUS_CODES
from collections.abc import Callable
from typing import Any


def retry(
    operation: Callable[[], Any],
    attempts: int = 2,
) -> Any:

    last_error = None

    for _ in range(attempts):
        try:
            return operation()

        except Exception as exc:
            last_error = exc

    raise last_error
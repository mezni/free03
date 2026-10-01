import random
import time
from collections.abc import Callable
from typing import TypeVar

from src.core.exceptions import (
    ProviderTimeoutError,
    TransientProviderError,
)
from src.providers.retryable import is_retryable_status

T = TypeVar("T")


DEFAULT_RETRYABLE: tuple[type[BaseException], ...] = (
    ProviderTimeoutError,
    TransientProviderError,
)


class RetryPolicy:
    """Retry with exponential backoff and jitter.

    The delay doubles per attempt (`base * 2**attempt`) up to
    `max_delay_seconds`, then a random fraction of that delay is added.

    The jitter is not cosmetic. Without it, every client that failed at
    the same moment retries at the same moment, and the retry storm
    arrives at the provider in synchronised waves.
    """

    def __init__(
        self,
        max_retries: int,
        delay_seconds: float,
        max_delay_seconds: float = 30.0,
        retryable_exceptions: tuple[type[BaseException], ...] = DEFAULT_RETRYABLE,
    ) -> None:
        if max_retries < 0:
            raise ValueError("max_retries must be zero or greater")

        if delay_seconds < 0:
            raise ValueError("delay_seconds must be zero or greater")

        if max_delay_seconds <= 0:
            raise ValueError("max_delay_seconds must be greater than zero")

        self._max_retries = max_retries
        self._delay_seconds = delay_seconds
        self._max_delay_seconds = max_delay_seconds
        self._retryable_exceptions = retryable_exceptions

    @property
    def max_retries(self) -> int:
        return self._max_retries

    @property
    def max_delay_seconds(self) -> float:
        return self._max_delay_seconds

    def delay(self, attempt: int) -> float:
        """Seconds to wait before `attempt` (0-based)."""
        if attempt < 0:
            raise ValueError("attempt must be zero or greater")

        exponential = self._delay_seconds * (2**attempt)

        capped = min(exponential, self._max_delay_seconds)

        if capped <= 0:
            return 0.0

        return capped + random.uniform(0, capped * 0.25)

    def execute(
        self,
        operation: Callable[[], T],
    ) -> T:
        attempts = 0

        while True:
            try:
                return operation()

            except self._retryable_exceptions:
                if attempts >= self._max_retries:
                    raise

                sleep_for = self.delay(attempts)

                attempts += 1

                if sleep_for > 0:
                    time.sleep(sleep_for)

            except Exception:
                # Includes any client-side rejection: those are
                # deterministic and would fail identically forever.
                raise

    @staticmethod
    def is_retryable_status(status_code: int) -> bool:
        """Expose status classification without duplicating the set."""
        return is_retryable_status(status_code)
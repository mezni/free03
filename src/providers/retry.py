from collections.abc import Callable
from time import sleep
from typing import TypeVar

from src.core.exceptions import (
    ProviderTimeoutError,
    TransientProviderError,
)

T = TypeVar("T")


DEFAULT_RETRYABLE: tuple[type[BaseException], ...] = (
    ProviderTimeoutError,
    TransientProviderError,
)


class RetryPolicy:
    def __init__(
        self,
        max_retries: int,
        delay_seconds: float,
        retryable_exceptions: tuple[
            type[BaseException], ...
        ] = DEFAULT_RETRYABLE,
    ) -> None:
        self._max_retries = max_retries
        self._delay_seconds = delay_seconds
        self._retryable_exceptions = retryable_exceptions

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

                attempts += 1

                if self._delay_seconds > 0:
                    sleep(self._delay_seconds)

            except Exception:
                raise
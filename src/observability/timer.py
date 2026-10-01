from time import perf_counter


class Timer:
    def __init__(self) -> None:
        self.duration_ms: float = 0.0
        self._started_at: float | None = None

    def __enter__(self) -> "Timer":
        self._started_at = perf_counter()

        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ) -> None:
        self.duration_ms = (
            perf_counter() - self._started_at
        ) * 1000
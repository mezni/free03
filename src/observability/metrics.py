from collections import defaultdict
from threading import Lock


class MetricsCollector:
    def __init__(self) -> None:
        self._counters: dict[str, int] = (
            defaultdict(int)
        )

        self._lock = Lock()

    def increment(
        self,
        name: str,
        value: int = 1,
    ) -> None:
        with self._lock:
            self._counters[name] += value

    def get(
        self,
        name: str,
    ) -> int:
        with self._lock:
            return self._counters.get(
                name,
                0,
            )

    def snapshot(self) -> dict[str, int]:
        with self._lock:
            return dict(self._counters)
from collections import defaultdict
from threading import Lock


class MetricsCollector:
    def __init__(self) -> None:
        self._counters: dict[str, int] = defaultdict(int)

        self._gauges: dict[str, float] = defaultdict(float)

        self._lock = Lock()

    def increment(
        self,
        name: str,
        value: int = 1,
    ) -> None:
        with self._lock:
            self._counters[name] += value

    def add(
        self,
        name: str,
        value: float,
    ) -> None:
        """Accumulate a fractional quantity, such as estimated cost.

        Token counts stay integers; money does not.
        """
        with self._lock:
            self._gauges[name] += value

    def get(
        self,
        name: str,
    ) -> int:
        with self._lock:
            return self._counters.get(
                name,
                0,
            )

    def get_total(
        self,
        name: str,
    ) -> float:
        with self._lock:
            return self._gauges.get(
                name,
                0.0,
            )

    def snapshot(self) -> dict[str, float]:
        with self._lock:
            return {**self._counters, **self._gauges}

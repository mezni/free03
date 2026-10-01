import pytest

from src.observability.metrics import MetricsCollector
from src.observability.registry import (
    get_metrics,
    reset_metrics,
    set_metrics,
)


class TestMetricsCollector:
    def test_metrics_counter(self) -> None:
        metrics = MetricsCollector()

        metrics.increment("rag.requests")
        metrics.increment("rag.requests")

        assert metrics.get("rag.requests") == 2

    def test_metrics_snapshot(self) -> None:
        metrics = MetricsCollector()

        metrics.increment("generation.requests")

        assert metrics.snapshot() == {
            "generation.requests": 1,
        }

    def test_increment_by_custom_value(self) -> None:
        metrics = MetricsCollector()

        metrics.increment("rag.errors", 5)

        assert metrics.get("rag.errors") == 5

    def test_get_missing_key_returns_zero(self) -> None:
        metrics = MetricsCollector()

        assert metrics.get("unknown") == 0

    def test_snapshot_is_copy(self) -> None:
        metrics = MetricsCollector()

        metrics.increment("retrieval.requests")

        snap = metrics.snapshot()
        snap["retrieval.requests"] = 999

        assert metrics.get("retrieval.requests") == 1

    def test_multiple_counters_independent(self) -> None:
        metrics = MetricsCollector()

        metrics.increment("a")
        metrics.increment("b", 3)

        assert metrics.snapshot() == {"a": 1, "b": 3}


class TestMetricsRegistry:
    def setup_method(self) -> None:
        reset_metrics()

    def teardown_method(self) -> None:
        reset_metrics()

    def test_get_metrics_singleton(self) -> None:
        first = get_metrics()
        second = get_metrics()

        assert first is second

    def test_set_metrics_replaces_singleton(self) -> None:
        replacement = MetricsCollector()

        set_metrics(replacement)

        assert get_metrics() is replacement

    def test_reset_metrics_recreates(self) -> None:
        original = get_metrics()
        reset_metrics()
        after = get_metrics()

        assert after is not original

    @pytest.mark.parametrize(
        "keys, values",
        [
            (["rag.requests"], [1]),
            (["a", "b", "a"], [1, 2, 3]),
        ],
    )
    def test_process_wide_accumulates(
        self,
        keys: list[str],
        values: list[int],
    ) -> None:
        m = get_metrics()

        for k, v in zip(keys, values, strict=False):
            m.increment(k, v)

        assert m.get("a") == 4 if "a" in keys else True
        assert (
            m.get(keys[0])
            == sum(v for k, v in zip(keys, values, strict=False) if k == keys[0])
            if keys
            else True
        )
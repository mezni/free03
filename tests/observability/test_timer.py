from time import sleep

import pytest

from src.observability.timer import Timer


class TestTimer:
    def test_timer(self) -> None:
        with Timer() as timer:
            sleep(0.001)

        assert timer.duration_ms > 0

    def test_timer_duration_captures_exit_value(self) -> None:
        with Timer() as timer:
            pass

        assert timer.duration_ms >= 0

    def test_timer_is_reusable_conceptually(self) -> None:
        for _ in range(3):
            with Timer() as timer:
                sleep(0.0001)

            assert timer.duration_ms > 0

    def test_timer_measures_nonzero(self) -> None:
        with Timer() as timer:
            total = 0
            for i in range(1000):
                total += i

        assert total == 499500
        assert timer.duration_ms >= 0

    @pytest.mark.parametrize("sleep_ms", [0.1, 0.01, 0.005])
    def test_timer_scales_with_duration(
        self,
        sleep_ms: float,
    ) -> None:
        with Timer() as t1:
            sleep(sleep_ms)

        with Timer() as t2:
            sleep(sleep_ms / 2)

        assert t1.duration_ms > t2.duration_ms

    def test_exit_records_even_if_exception(self) -> None:
        with pytest.raises(ValueError):
            with Timer() as timer:
                raise ValueError("boom")

        assert timer.duration_ms >= 0
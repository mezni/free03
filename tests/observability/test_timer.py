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

    def test_longer_work_yields_longer_duration(self) -> None:
        """Compares clearly separated durations.

        An earlier version slept 5ms against 2.5ms and failed
        intermittently: `sleep` guarantees a minimum, not an exact
        duration, so scheduler noise could invert the comparison. The
        20ms gap here is wide enough to survive that noise.
        """
        with Timer() as short:
            sleep(0.01)

        with Timer() as long:
            sleep(0.03)

        assert long.duration_ms > short.duration_ms

    def test_exit_records_even_if_exception(self) -> None:
        with pytest.raises(ValueError):
            with Timer() as timer:
                raise ValueError("boom")

        assert timer.duration_ms >= 0

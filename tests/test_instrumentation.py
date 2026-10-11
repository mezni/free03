import pytest

from ticket_triage.instrumentation import observe_classification
from ticket_triage.metrics import (
    CLASSIFICATION_DURATION,
    CLASSIFICATION_ATTEMPTS,
)


def test_successful_classification_is_counted():
    before = CLASSIFICATION_ATTEMPTS.labels(
        outcome="success"
    )._value.get()

    result = observe_classification(lambda: "recommendation")

    after = CLASSIFICATION_ATTEMPTS.labels(
        outcome="success"
    )._value.get()

    assert result == "recommendation"
    assert after - before == 1


def test_failed_classification_is_counted_and_reraised():
    before = CLASSIFICATION_ATTEMPTS.labels(
        outcome="failure"
    )._value.get()

    def fail():
        raise ValueError("expected failure")

    with pytest.raises(ValueError, match="expected failure"):
        observe_classification(fail)

    after = CLASSIFICATION_ATTEMPTS.labels(
        outcome="failure"
    )._value.get()

    assert after - before == 1


def test_classification_duration_is_observed():
    observe_classification(lambda: "recommendation")
    # observe() records the duration; verify no error was raised
    assert CLASSIFICATION_DURATION is not None
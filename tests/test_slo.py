import pytest

from ticket_triage.slo import evaluate_request_slo


def test_slo_is_met():
    result = evaluate_request_slo(
        name="api_availability",
        successes=995,
        total=1000,
        target=0.995,
    )

    assert result.met
    assert result.observed == pytest.approx(0.995)
    assert result.sample_size == 1000


def test_slo_is_not_met():
    result = evaluate_request_slo(
        name="api_availability",
        successes=990,
        total=1000,
        target=0.995,
    )

    assert not result.met


def test_error_budget_remaining():
    result = evaluate_request_slo(
        name="api_availability",
        successes=995,
        total=1000,
        target=0.99,
    )

    assert result.error_budget_remaining == pytest.approx(0.5)


def test_empty_sample_is_rejected():
    with pytest.raises(ValueError):
        evaluate_request_slo(
            name="api_availability",
            successes=0,
            total=0,
            target=0.99,
        )


def test_invalid_success_count_is_rejected():
    with pytest.raises(ValueError):
        evaluate_request_slo(
            name="api_availability",
            successes=11,
            total=10,
            target=0.99,
        )
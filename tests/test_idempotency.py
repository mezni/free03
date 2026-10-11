import pytest

from ticket_triage.idempotency import routing_idempotency_key


def test_same_operation_has_same_key():
    first = routing_idempotency_key("case-123", 1)
    second = routing_idempotency_key("case-123", 1)

    assert first == second


def test_new_recommendation_has_new_key():
    first = routing_idempotency_key("case-123", 1)
    second = routing_idempotency_key("case-123", 2)

    assert first != second


def test_different_cases_have_different_keys():
    first = routing_idempotency_key("case-123", 1)
    second = routing_idempotency_key("case-456", 1)

    assert first != second


def test_empty_case_id_is_rejected():
    with pytest.raises(ValueError):
        routing_idempotency_key("   ", 1)


def test_non_positive_version_is_rejected():
    with pytest.raises(ValueError):
        routing_idempotency_key("case-123", 0)

from support_agent.memory_policy import (
    should_store_memory,
)
from support_agent.models import MemoryCandidate


def test_valid_memory_is_accepted():

    candidate = MemoryCandidate(
        customer_id="C002",
        key="preferred_contact_method",
        value="email",
        confidence=0.95,
    )

    assert should_store_memory(candidate) is True


def test_low_confidence_memory_is_rejected():

    candidate = MemoryCandidate(
        customer_id="C002",
        key="preferred_contact_method",
        value="email",
        confidence=0.50,
    )

    assert should_store_memory(candidate) is False


def test_unknown_memory_key_is_rejected():

    candidate = MemoryCandidate(
        customer_id="C002",
        key="current_emotion",
        value="frustrated",
        confidence=0.99,
    )

    assert should_store_memory(candidate) is False


def test_empty_value_is_rejected():

    candidate = MemoryCandidate(
        customer_id="C002",
        key="preferred_contact_method",
        value="",
        confidence=0.95,
    )

    assert should_store_memory(candidate) is False


def test_missing_customer_id_is_rejected():

    candidate = MemoryCandidate(
        customer_id="",
        key="preferred_contact_method",
        value="email",
        confidence=0.95,
    )

    assert should_store_memory(candidate) is False
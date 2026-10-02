from support_agent.models import (
    MemoryCandidate,
    MemoryExtractionResult,
)


def test_memory_candidate():
    candidate = MemoryCandidate(
        customer_id="C002",
        key="preferred_contact_method",
        value="email",
        confidence=0.95,
    )

    assert candidate.customer_id == "C002"
    assert candidate.key == "preferred_contact_method"
    assert candidate.value == "email"


def test_empty_memory_result():
    result = MemoryExtractionResult(
        memories=[]
    )

    assert result.memories == []


def test_multiple_memory_candidates():
    result = MemoryExtractionResult(
        memories=[
            MemoryCandidate(
                customer_id="C002",
                key="preferred_contact_method",
                value="email",
                confidence=0.95,
            ),
            MemoryCandidate(
                customer_id="C002",
                key="preferred_language",
                value="English",
                confidence=0.90,
            ),
        ]
    )

    assert len(result.memories) == 2
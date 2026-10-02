from support_agent.customer_memory import MEMORIES
from support_agent.memory_manager import (
    process_message_for_memory,
)
from support_agent.memory_policy import (
    should_store_memory,
)
from support_agent.models import (
    MemoryCandidate,
    MemoryExtractionResult,
)


def test_process_message_stores_valid_memory(
    monkeypatch,
):
    MEMORIES.clear()

    def fake_extraction(message):
        return MemoryExtractionResult(
            memories=[
                MemoryCandidate(
                    customer_id="C002",
                    key="preferred_contact_method",
                    value="email",
                    confidence=0.95,
                )
            ]
        )

    monkeypatch.setattr(
        "support_agent.memory_manager.extract_memory_candidates",
        fake_extraction,
    )

    memories = process_message_for_memory(
        "I prefer email."
    )

    assert len(memories) == 1
    assert memories[0].customer_id == "C002"
    assert memories[0].value == "email"


def test_process_message_rejects_invalid_memory(
    monkeypatch,
):
    MEMORIES.clear()

    def fake_extraction(message):
        return MemoryExtractionResult(
            memories=[
                MemoryCandidate(
                    customer_id="C002",
                    key="current_emotion",
                    value="frustrated",
                    confidence=0.99,
                )
            ]
        )

    monkeypatch.setattr(
        "support_agent.memory_manager.extract_memory_candidates",
        fake_extraction,
    )

    memories = process_message_for_memory(
        "I'm frustrated."
    )

    assert memories == []
    assert len(MEMORIES) == 0
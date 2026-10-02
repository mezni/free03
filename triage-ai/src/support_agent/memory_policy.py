from enum import Enum

from support_agent.models import (
    CustomerMemory,
    MemoryCandidate,
)


class MemoryDecision(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    KEEP_EXISTING = "keep_existing"


SOURCE_PRIORITY = {
    "customer_statement": 4,
    "imported_data": 3,
    "support_agent": 2,
    "system": 1,
}


def should_store_memory(
    candidate: MemoryCandidate,
) -> bool:

    if not candidate.customer_id:
        return False

    if not candidate.key:
        return False

    if not candidate.value.strip():
        return False

    if candidate.confidence < MIN_MEMORY_CONFIDENCE:
        return False

    if candidate.key not in ALLOWED_MEMORY_KEYS:
        return False

    return True


def resolve_memory_conflict(
    existing: CustomerMemory,
    candidate: MemoryCandidate,
) -> MemoryDecision:

    existing_source_priority = SOURCE_PRIORITY.get(
        existing.source.value,
        0,
    )

    candidate_source_priority = SOURCE_PRIORITY.get(
        candidate.source.value,
        0,
    )

    if candidate_source_priority > existing_source_priority:
        return MemoryDecision.UPDATE

    if candidate_source_priority < existing_source_priority:
        return MemoryDecision.KEEP_EXISTING

    if candidate.confidence > existing.confidence:
        return MemoryDecision.UPDATE

    return MemoryDecision.KEEP_EXISTING
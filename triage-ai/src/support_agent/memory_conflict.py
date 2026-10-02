from support_agent.models import MemoryDecision, MemorySource, MemoryType


def resolve_memory_conflict(
    existing,
    candidate_source: MemorySource,
    candidate_confidence: float,
) -> MemoryDecision:

    existing_source_priority = {
        MemorySource.CUSTOMER_STATEMENT: 4,
        MemorySource.IMPORTED_DATA: 3,
        MemorySource.SUPPORT_AGENT: 2,
        MemorySource.SYSTEM: 1,
    }

    current_priority = existing_source_priority[
        existing.source
    ]

    new_priority = existing_source_priority[
        candidate_source
    ]

    should_update = (
        new_priority > current_priority
        or (
            new_priority == current_priority
            and candidate_confidence > existing.confidence
        )
    )

    if should_update:
        return MemoryDecision.UPDATE

    return MemoryDecision.KEEP_EXISTING
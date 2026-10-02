from support_agent.memory_service import MemoryService
from support_agent.models import (
    EvaluationStatus,
    MemoryEvaluationResult,
)


def evaluate_memory_case(
    *,
    name: str,
    customer_id: str,
    query: str,
    expected_memory_key: str | None,
) -> MemoryEvaluationResult:

    service = MemoryService()

    memories = service.retrieve(
        customer_id=customer_id,
        query=query,
    )

    keys = {
        item.memory.key
        for item in memories
    }

    if expected_memory_key is None:
        passed = len(keys) == 0
    else:
        passed = expected_memory_key in keys

    status = (
        EvaluationStatus.PASS
        if passed
        else EvaluationStatus.FAIL
    )

    return MemoryEvaluationResult(
        name=name,
        status=status,
        details=(
            f"Retrieved memory keys: {sorted(keys)}"
        ),
    )
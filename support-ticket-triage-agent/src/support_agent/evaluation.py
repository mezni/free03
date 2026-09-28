import json
from pathlib import Path

from support_agent.models.evaluation import (
    EvaluationCase,
    EvaluationResult,
)
from support_agent.models.ticket import (
    TicketExtraction,
    TriageDecision,
)


def load_evaluation_cases(
    path: str,
) -> list[EvaluationCase]:

    file_path = Path(path)

    with file_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        data = json.load(file)

    return [
        EvaluationCase.model_validate(item)
        for item in data
    ]


def evaluate_extraction(
    actual: TicketExtraction,
    expected: EvaluationCase,
) -> dict[str, bool]:

    return {
        "product": (
            actual.product
            == expected.expected_product
        ),
        "priority": (
            actual.priority
            == expected.expected_priority
        ),
    }


def evaluate_triage(
    actual: TriageDecision,
    expected: EvaluationCase,
) -> dict[str, bool]:

    return {
        "category": (
            actual.category
            == expected.expected_category
        ),
        "urgency": (
            actual.urgency
            == expected.expected_urgency
        ),
        "escalation": (
            actual.needs_escalation
            == expected.expected_escalation
        ),
    }


def evaluate_case(
    extraction,
    triage,
    expected: EvaluationCase,
) -> EvaluationResult:

    extraction_checks = evaluate_extraction(
        extraction,
        expected,
    )

    triage_checks = evaluate_triage(
        triage,
        expected,
    )

    checks = {
        **extraction_checks,
        **triage_checks,
    }

    passed = all(checks.values())

    return EvaluationResult(
        case_id=expected.case_id,
        passed=passed,
        checks=checks,
    )
from typing import Any, Literal

from pydantic import BaseModel


class EvaluationCase(BaseModel):
    case_id: str
    ticket_id: str
    expected_category: str
    expected_urgency: str
    expected_priority: str
    expected_product: str
    expected_escalation: bool


class EvaluationResult(BaseModel):
    case_id: str
    passed: bool
    checks: dict[str, bool]
    details: dict[str, Any] = {}


class EvaluationSummary(BaseModel):
    total_cases: int
    passed_cases: int
    failed_cases: int
    pass_rate: float
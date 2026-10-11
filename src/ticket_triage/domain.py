from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum


class Priority(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class CaseStatus(StrEnum):
    RECEIVED = "received"
    PROCESSING = "processing"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    ROUTING = "routing"
    COMPLETED = "completed"
    MANUAL_REVIEW = "manual_review"


class DecisionType(StrEnum):
    APPROVED = "approved"
    REJECTED = "rejected"


@dataclass(frozen=True)
class Ticket:
    ticket_id: str
    subject: str
    description: str


@dataclass(frozen=True)
class Recommendation:
    category: str
    priority: Priority
    destination: str
    rationale: str


@dataclass(frozen=True)
class ApprovalDecision:
    decision_id: str
    case_id: str
    recommendation_version: int
    actor_id: str
    decision: DecisionType
    decided_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    comment: str | None = None


class RoutingStatus(StrEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    OUTCOME_UNKNOWN = "outcome_unknown"
    RECONCILIATION_REQUIRED = "reconciliation_required"


@dataclass
class RoutingOperation:
    operation_id: str
    case_id: str
    approval_decision_id: str
    idempotency_key: str
    status: RoutingStatus = RoutingStatus.PENDING
    attempts: int = 0
    external_operation_id: str | None = None
    error_message: str | None = None


@dataclass
class TriageCase:
    case_id: str
    ticket: Ticket
    status: CaseStatus = CaseStatus.RECEIVED
    recommendation: Recommendation | None = None
    recommendation_version: int = 0
    approval_decision: ApprovalDecision | None = None

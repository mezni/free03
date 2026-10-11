from dataclasses import dataclass
from enum import Enum


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class CaseStatus(str, Enum):
    RECEIVED = "received"
    PROCESSING = "processing"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    ROUTING = "routing"
    COMPLETED = "completed"
    MANUAL_REVIEW = "manual_review"


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

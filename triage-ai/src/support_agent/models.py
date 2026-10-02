import uuid
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class MemorySource(str, Enum):
    CUSTOMER_STATEMENT = "customer_statement"
    SUPPORT_AGENT = "support_agent"
    SYSTEM = "system"
    IMPORTED_DATA = "imported_data"


class MemoryType(str, Enum):
    PREFERENCE = "preference"
    PROFILE = "profile"
    ACCOUNT = "account"
    PRODUCT = "product"


class MemoryDecision(str, Enum):
    KEEP_EXISTING = "keep_existing"
    UPDATE = "update"


class EvaluationStatus(str, Enum):
    PASS = "pass"
    FAIL = "fail"


class MemoryEvaluationResult(BaseModel):
    name: str
    status: EvaluationStatus
    details: str


class BehavioralEvaluation(BaseModel):
    passed: bool
    reason: str


class MemoryCandidate(BaseModel):
    customer_id: str
    key: str
    value: str
    memory_type: MemoryType
    source: MemorySource
    confidence: float


class ExtractedTicket:
    def __init__(
        self,
        customer_id: str | None = None,
        product: str | None = None,
        sentiment: str | None = None,
        priority: str | None = None,
        category: str | None = None,
    ):
        self.customer_id = customer_id
        self.product = product
        self.sentiment = sentiment
        self.priority = priority
        self.category = category


class CustomerMemory:
    def __init__(
        self,
        memory_id: str,
        customer_id: str,
        key: str,
        value: str,
        memory_type: MemoryType,
        source: MemorySource,
        confidence: float,
        created_at: datetime,
        updated_at: datetime,
        expires_at: datetime | None = None,
    ):
        self.memory_id = memory_id
        self.customer_id = customer_id
        self.key = key
        self.value = value
        self.memory_type = memory_type
        self.source = source
        self.confidence = confidence
        self.created_at = created_at
        self.updated_at = updated_at
        self.expires_at = expires_at


class MemoryExtractionResult(BaseModel):
    memories: list[MemoryCandidate]


class RetrievedMemory(BaseModel):
    memory: CustomerMemory
    relevance_score: int

    model_config = {"arbitrary_types_allowed": True}
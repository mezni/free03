import uuid
from typing import TypeVar, List
from pydantic import BaseModel


UUIDType = TypeVar("UUIDType", bound=uuid.UUID)


class Tag(BaseModel):
    tag_code: UUIDType
    tag_type: str
    tag_name: str
    tag_value: str


class Cost(BaseModel):
    cost_code: UUIDType
    cost_type: str
    cost_value: float
    cost_currency: str


class CostRecord(BaseModel):

    cost_code: UUIDType
    org_name: str
    provider_name: str
    period_name: str
    account_id: str
    account_name: str
    service_name: str
    resource_id: str
    resource_name: str
    tags: List[Tag]
    cost: List[Cost]

import uuid
from datetime import datetime
from typing import TypeVar, List, Dict
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


class Batch(BaseModel):
    batch_code: UUIDType
    batch_name: str
    batch_start_time: datetime
    batch_end_time: datetime
    batch_status: str
    exit_status: str
    exit_message: str


class CostRecordBatch(BaseModel):
    batch_code: UUIDType
    cost_record_list: List[CostRecord]
    org_list: List[Dict]
    provider_list: List[Dict]
    period_list: List[Dict]
    service_list: List[Dict]
    resource_list: List[Dict]
    region_list: List[Dict]

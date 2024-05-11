import uuid
from typing import TypeVar
from pydantic import BaseModel
from datetime import datetime

UUIDType = TypeVar("UUIDType", bound=uuid.UUID)


class Organisation(BaseModel):
    org_code: UUIDType
    org_name: str


class Provider(BaseModel):
    provider_code: UUIDType
    provider_name: str


class Period(BaseModel):
    period_code: UUIDType
    period_name: str
    period_date: datetime
    period_day: int
    period_month: int
    period_year: int
    period_quarter: int
    period_day_of_week: int
    period_day_of_year: int
    period_week_of_year: int
    period_is_holiday: bool


class Service(BaseModel):
    service_code: UUIDType
    service_name: str
    provider_code: UUIDType

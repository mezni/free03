""" Usage entities module
"""

import uuid
from typing import TypeVar


from datetime import datetime
from pydantic import BaseModel

UUIDType = TypeVar("UUIDType", bound=uuid.UUID)


def generate_uuid() -> UUIDType:
    return uuid.uuid4()


class Period(BaseModel):
    """Definition of the Period entity"""

    period_code: UUIDType
    period_name: str
    period_date: datetime
    period_day: int
    period_month: int
    period_year: int
    period_is_holiday: bool

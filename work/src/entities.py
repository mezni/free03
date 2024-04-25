""" Usage entities module
"""

import uuid
from datetime import datetime
from pydantic import BaseModel


class Period(BaseModel):
    """Definition of the Period entity"""

    period_code: uuid.UUID
    period_name: str
    period_date: datetime
    period_day: int
    period_month: int
    period_year: int
    period_is_holiday: bool

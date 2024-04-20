""" Module for Period entity
"""

from datetime import datetime
from dataclasses import dataclass, asdict
from src.domain.value_objects import CodeId


@dataclass
class Period:
    """Definition of the Period entity"""

    period_code: CodeId
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

    @classmethod
    def from_dict(cls, data):
        """Convert data from a dictionary"""
        return cls(**data)

    def to_dict(self):
        """Convert data into dictionary"""
        return asdict(self)

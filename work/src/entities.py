""" Module for entities

"""

from datetime import datetime
from dataclasses import dataclass, asdict
from uuid import UUID as CodeId


@dataclass
class Period:
    """Definition of the Period entity"""

    period_code: CodeId
    period_name: str
    period_is_holiday: bool = False

    @property
    def period_date(self):
        return datetime.strptime(self.period_name, "%Y-%m-%d")

    @property
    def period_day(self):
        return self.period_date.day

    @property
    def period_month(self):
        return self.period_date.month

    @property
    def period_year(self):
        return self.period_date.year

    @property
    def period_quarter(self):
        return self.period_date.month // 3 + 1

    @property
    def period_day_of_week(self):
        return self.period_date.weekday() + 1

    @property
    def period_day_of_year(self):
        return self.period_date.timetuple().tm_yday

    @property
    def period_week_of_year(self):
        return self.period_date.isocalendar()[1]

    @classmethod
    def from_dict(cls, data):
        """Convert data from a dictionary"""
        return cls(**data)

    def to_dict(self):
        """Convert data into dictionary"""
        return {
            "period_code": self.period_code,
            "period_name": self.period_name,
            "period_date": self.period_date,
            "period_day": self.period_day,
            "period_month": self.period_month,
            "period_year": self.period_year,
            "period_quarter": self.period_quarter,
            "period_day_of_week": self.period_day_of_week,
            "period_day_of_year": self.period_day_of_year,
            "period_week_of_year": self.period_week_of_year,
            "period_is_holiday": self.period_is_holiday,
        }

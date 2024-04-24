from datetime import datetime
from dataclasses import dataclass
from uuid import UUID as CodeId


@dataclass
class Period:

    period_code: CodeId
    period_name: str
    period_date: datetime.datetime
    period_is_holiday: bool = False

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
            "period_is_holiday": self.period_is_holiday,
        }

from datetime import datetime
from dataclasses import dataclass, asdict
from uuid import UUID as CodeId


@dataclass
class Period:

    period_code: CodeId
    period_name: str
    period_date: datetime.datetime
    period_is_holiday: bool = False

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def to_dict(self):
        return asdict(self)

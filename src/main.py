import uuid
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict


@dataclass
class Period:
    """Definition of the Period entity"""

    period_code: uuid.UUID
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


@dataclass
class PeriodInputDto:
    period_name: str

    def to_dict(self):
        """Convert data into dictionary"""
        return asdict(self)


@dataclass
class PeriodOutputDto:
    """Output Dto for create profession"""

    period: Period


class PeriodPresenter:
    @staticmethod
    def dto_to_entity(period_dto):
        period_code = uuid.uuid4()
        period_name = period_dto.period_name
        period_date = datetime.strptime(period_dto.period_name, "%Y-%m-%d")
        period_day = period_date.day
        period_month = period_date.month
        period_year = period_date.year
        period_quarter = period_date.month // 3 + 1
        period_day_of_week = period_date.weekday() + 1
        period_day_of_year = period_date.timetuple().tm_yday
        period_week_of_year = period_date.isocalendar()[1]
        period_is_holiday = False
        period = Period(
            period_code,
            period_name,
            period_date,
            period_day,
            period_month,
            period_year,
            period_quarter,
            period_day_of_week,
            period_day_of_year,
            period_week_of_year,
            period_is_holiday,
        )
        return period


class PeriodRepository:
    def __init__(self):
        self.periods = []

    def add(self, period):
        self.periods.append(period)

    def get_period_by_name(self, period_name):
        l = [p for p in self.periods if p.period_name == period_name]
        if l:
            return l[0]
        else:
            return None

    def list(self):
        return self.periods


def main():
    data = [
        {"period_name": "2024-04-01"},
        {"period_name": "2024-04-01"},
        {"period_name": "2024-04-02"},
        {"period_name": "2024-04-03"},
        {"period_name": "2024-04-03"},
    ]
    period_repo = PeriodRepository()

    for d in data:
        period_saved = period_repo.get_period_by_name(d["period_name"])
        if not period_saved:
            period_dto = PeriodInputDto(d["period_name"])
            period = PeriodPresenter.dto_to_entity(period_dto)
            period_repo.add(period)
        else:
            period = period_saved

    period_list = period_repo.list()
    for p in period_list:
        print(f"period= {p.period_code} - {p.period_name} - {p.period_date}")

main()

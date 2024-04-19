import uuid
from dataclasses import dataclass, asdict


@dataclass
class Period:
    """Definition of the Period entity"""

    period_code: uuid.UUID
    period_name: str

    @classmethod
    def from_dict(cls, data):
        """Convert data from a dictionary"""
        return cls(**data)

    def to_dict(self):
        """Convert data into dictionary"""
        return asdict(self)


class PeriodRepository:
    def __init__(self):
        self.periods = []

    def add(self, period):
        self.periods.append(period)

    def get_by_period_name(self, period_name):
        l=[p for p in self.periods if p.period_name == period_name]
        if l:
            return l[0]
        else:
            return None
            

    def list(self):
        return self.periods


class UsageLoadUseCase:
    def __init__(self, period_repo):
        self.period_repo = period_repo

    def execute(self, data):
        for d in data:
            period_saved=self.period_repo.get_by_period_name( d["period_name"])
            if not period_saved:
                period = Period.from_dict(
                    {"period_code": uuid.uuid4(), "period_name": d["period_name"]}
                )
                self.period_repo.add(period)
            else:
                period=period_saved


def main():
    data = [
        {"period_name": "2024-04-01"},
        {"period_name": "2024-04-01"},
        {"period_name": "2024-04-02"},
        {"period_name": "2024-04-03"},
        {"period_name": "2024-04-03"},
    ]
    period_repo = PeriodRepository()
    load_uc = UsageLoadUseCase(period_repo)
    load_uc.execute(data)

    # List periods
    period_list = period_repo.list()
    for p in period_list:
        print(f"period= {p.period_code} - {p.period_name}")


main()

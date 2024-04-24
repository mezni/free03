import asyncio
import uuid
from datetime import datetime, timedelta
from typing import List
from pydantic import BaseModel, ValidationError, field_validator


class PeriodIn(BaseModel):
    period_name: str


from datetime import datetime


class PeriodIntervalIn(BaseModel):
    period_interval: List[str]
    period_interval_min: datetime = None
    period_interval_max: datetime = None

    def model_post_init(self, __context) -> None:
        period_interval_min = datetime(2200, 1, 1)
        period_interval_max = datetime(1900, 1, 1)
        if len(self.period_interval) != 0:
            for p in self.period_interval:
                p_date = datetime.strptime(p, "%Y-%m-%d")
                if p_date < period_interval_min:
                    period_interval_min = p_date
                if p_date > period_interval_max:
                    period_interval_max = p_date
            self.period_interval_min = period_interval_min
            self.period_interval_max = period_interval_max


class PeriodIn(BaseModel):
    period_code: uuid.UUID = None
    period_name: str
    period_date: datetime = None
    period_day: int = None
    period_month: int = None
    period_year: int = None

    def model_post_init(self, __context) -> None:
        self.period_code = uuid.uuid4()
        self.period_date = datetime.strptime(self.period_name, "%Y-%m-%d")
        self.period_day = self.period_date.day
        self.period_month = self.period_date.month
        self.period_year = self.period_date.year


class PeriodOut(BaseModel):
    period_code: uuid.UUID
    period_name: str
    period_date: datetime
    period_day: int
    period_month: int
    period_year: int


class PeriodIntervalOut(BaseModel):
    period_interval: List[PeriodOut]


def create_period_interval(period_interval_in: PeriodIntervalIn) -> PeriodIntervalOut:
    start_date = period_interval_in.period_interval_min
    end_date = period_interval_in.period_interval_max
    day_count = (end_date - start_date).days + 1
    for curr_date in [
        d
        for d in (start_date + timedelta(n) for n in range(day_count))
        if d <= end_date
    ]:
        p_in = PeriodIn(period_name=curr_date.strftime("%Y-%m-%d"))
        p_out = PeriodOut(**p_in.model_dump())
        print(p_out.model_dump())


async def main():
    #    period_list = []
    period_list = ["2024-04-21", "2024-04-02", "2024-04-22"]
    period_interval_in = PeriodIntervalIn(period_interval=period_list)
    print(period_interval_in.model_dump())
    period_interval_out = create_period_interval(period_interval_in)


asyncio.run(main())

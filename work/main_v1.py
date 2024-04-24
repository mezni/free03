import asyncio
from datetime import datetime
from typing import List
from pydantic import BaseModel, ValidationError, ValidationInfo, field_validator


class PeriodName(BaseModel):
    period_name: str

    @field_validator("period_name")
    def period_name_format(cls, v: str, info: ValidationInfo) -> str:
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except:
            raise ValueError("Invalid format")
        return v


class PeriodNameList(BaseModel):
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


async def main():
    print("# Enter")
    p = PeriodName(period_name="2024-04-12")
    l=PeriodNameList(period_interval=["2024-04-20", "2024-04-01", "2024-04-10"])
    print(l)


asyncio.run(main())

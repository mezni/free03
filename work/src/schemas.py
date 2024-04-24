import uuid
from datetime import datetime
from pydantic import BaseModel
from src.entities import Period


class PeriodSchemaIn(BaseModel):
    period_code: uuid.UUID = None
    period_name: str
    period_date: datetime = None
    period_day: int = None
    period_month: int = None
    period_year: int = None
    period_is_holiday: bool = False

    def model_post_init(self, __context) -> None:
        self.period_code = uuid.uuid4()
        self.period_date = datetime.strptime(self.period_name, "%Y-%m-%d")
        self.period_day = self.period_date.day
        self.period_month = self.period_date.month
        self.period_year = self.period_date.year


class PeriodSchemaOut(Period):
    pass

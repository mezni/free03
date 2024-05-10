import uuid
from pydantic import BaseModel
from entities import UUIDType, Organisation, Provider, Period
from datetime import datetime


def generate_uuid() -> UUIDType:
    return uuid.uuid4()


class OrganisationInputDto(BaseModel):
    org_code: UUIDType = None
    org_name: str

    def model_post_init(self, __context) -> None:
        self.org_code = generate_uuid()


class OrganisationOutputDto(Organisation):
    pass


class ProviderInputDto(BaseModel):
    provider_code: UUIDType = None
    provider_name: str

    def model_post_init(self, __context) -> None:
        self.provider_code = generate_uuid()


class ProviderOutputDto(Provider):
    pass


class PeriodInputDTO(BaseModel):
    period_code: UUIDType = None
    period_name: str
    period_date: datetime = None
    period_day: int = None
    period_month: int = None
    period_year: int = None
    period_quarter: int = None
    period_day_of_week: int = None
    period_day_of_year: int = None
    period_week_of_year: int = None
    period_is_holiday: bool = False

    def model_post_init(self, __context) -> None:
        self.period_code = generate_uuid()
        self.period_date = datetime.strptime(self.period_name, "%Y-%m-%d")
        self.period_day = self.period_date.day
        self.period_month = self.period_date.month
        self.period_year = self.period_date.year
        self.period_quarter = self.period_date.month // 3 + 1
        self.period_day_of_week = self.period_date.weekday() + 1
        self.period_day_of_year = self.period_date.timetuple().tm_yday
        self.period_week_of_year = self.period_date.isocalendar()[1]


class PeriodOutputtDTO(Period):
    pass

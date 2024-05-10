import uuid
import asyncio
from datetime import date, timedelta
from db_config import init_db, create_db_engine
from sqlalchemy.orm import sessionmaker
from models import OrganisationModel, ProviderModel
from sqlalchemy.ext.asyncio import AsyncSession


from datetime import datetime
from pydantic import BaseModel
from src.entities import Period, UUIDType, generate_uuid


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


def date_range_list(start_date, end_date):
    # Return list of datetime.date objects (inclusive) between start_date and end_date (inclusive).
    date_list = []
    curr_date = start_date
    while curr_date <= end_date:
        date_list.append(curr_date)
        curr_date += timedelta(days=1)
    return date_list


async def create_orgs(engine):
    AsyncSessionLocal = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    async with AsyncSessionLocal() as session:
        async with session.begin():
            new_org = OrganisationModel(org_code=uuid.uuid4(), org_name="falcon tech")
            session.add(new_org)


async def create_providers(engine):
    AsyncSessionLocal = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    async with AsyncSessionLocal() as session:
        async with session.begin():
            for provider_name in ["aws", "azure", "oci"]:
                provider_org = ProviderModel(
                    provider_code=uuid.uuid4(), provider_name=provider_name
                )
                session.add(provider_org)


async def main():
    db_url = "sqlite+aiosqlite:///_dwh.db"
    engine = await create_db_engine(db_url)
    #    await init_db(engine)
    #    await create_orgs(engine)
    await create_providers(engine)

    start_date = date(year=2023, month=9, day=1)
    stop_date = date(year=2024, month=9, day=1)
    date_list = date_range_list(start_date, stop_date)


asyncio.run(main())

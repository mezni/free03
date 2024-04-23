import uuid
import asyncio
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from src.database import init_db, get_session
from src.models import PeriodModel
from src.entities import Period
from src.schemas import CreatePeriodIn
from sqlalchemy import select
from typing import List

async def get_periods_interval(period_list):
    period_name_min = None
    period_name_max = None
    period_date_min = datetime(2200, 1, 1)
    period_date_max = datetime(1900, 1, 1)

    for p in period_list:
        period_date = datetime.strptime(p, "%Y-%m-%d")
        if period_date < period_date_min:
            period_date_min = period_date
        if period_date > period_date_max:
            period_date_max = period_date

    if period_date_min:
        period_name_min = period_date_min.strftime("%Y-%m-%d")
    if period_date_max:
        period_name_max = period_date_max.strftime("%Y-%m-%d")

    return period_name_min, period_name_max


async def load_periods(
    async_session: async_sessionmaker[AsyncSession],
    period_name_min: str,
    period_name_max: str,
):
    total_days = (
        datetime.strptime(period_name_max, "%Y-%m-%d")
        - datetime.strptime(period_name_min, "%Y-%m-%d")
    ).days + 1
    async with async_session() as session:
        for day_number in range(total_days):
            current_date = (
                datetime.strptime(period_name_min, "%Y-%m-%d")
                + timedelta(days=day_number)
            ).date()
            print(current_date)
            session.add(PeriodModel(period_code=uuid.uuid4(),period_name=current_date.strftime("%Y-%m-%d")))
            await  session.commit()
            stmt = select(PeriodModel)#.where(PeriodModel.period_name == current_date.strftime("%Y-%m-%d"))
            result = await session.execute(stmt)


async def list_periods(
    async_session: async_sessionmaker[AsyncSession],
    period_name_min: str,
    period_name_max: str,
):
    total_days = (
        datetime.strptime(period_name_max, "%Y-%m-%d")
        - datetime.strptime(period_name_min, "%Y-%m-%d")
    ).days + 1
    async with async_session() as session:
        stmt = select(PeriodModel)#.where(PeriodModel.period_name == current_date.strftime("%Y-%m-%d"))
        result = await session.execute(stmt)
        return result.fetchall()

async def main():
    await init_db()
    session = await get_session()
    period_list = ["2024-04-10", "2024-04-04", "2024-04-01"]
    period_name_min, period_name_max = await get_periods_interval(period_list)

    await load_periods(session, period_name_min, period_name_max)

    xx=await list_periods(session, period_name_min, period_name_max)
    print (xx)

asyncio.run(main())

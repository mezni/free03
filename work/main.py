import uuid
import asyncio
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from src.database import init_db, get_session
from src.models import Period as PeriodModel
from src.entities import Period
from src.schemas import CreatePeriodIn
from sqlalchemy import select


async def create_moteur(
    async_session: async_sessionmaker[AsyncSession], period_name: str
):
    item_db = PeriodModel(period_code=uuid.uuid4(), period_name=period_name)
    async with async_session() as session:
        async with session.begin():
            session.add(item_db)
            return item_db

async def list_periods(
    async_session: async_sessionmaker[AsyncSession]
):
    async with async_session() as session:
        stmt = select(PeriodModel)  # .order_by(A.id).options(selectinload(A.bs))
        result = await session.execute(stmt)  
        return result
# async def period_uc(period_dto):
#    x=Period(period_code=uuid.uuid4(), period_name=period_dto.period_name)
#    return x


async def periods_interval(
    async_session: async_sessionmaker[AsyncSession],
    period_name_min: str,
    period_name_max: str,
):
    pass


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


async def period_uc(period_list):
    session = await get_session()
    period_name_min, period_name_max = await get_periods_interval(period_list)
    x=await create_moteur(session,period_name_min)
    total_days = (
        datetime.strptime(period_name_max, "%Y-%m-%d")
        - datetime.strptime(period_name_min, "%Y-%m-%d")
    ).days + 1
    result=await list_periods(session)
    for a in result.scalars():
        print (a.period_code)
    


#    for day_number in range(total_days):
#        current_date = (
#            datetime.strptime(period_name_min, "%Y-%m-%d") + timedelta(days=day_number)
#        ).date()
#        print(current_date)


async def main():
    await init_db()
    session = await get_session()
    period_list = ["2024-04-20", "2024-04-10", "2024-04-01"]
    uc = await period_uc(period_list)


#    period_name = "2024-04-05"
#    period_dto=CreatePeriodIn(period_name)
#    uc=await period_uc(period_dto)
#    print (uc.period_day)
#    await create_moteur(session, "2024-04-05")


asyncio.run(main())

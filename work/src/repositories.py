import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select
from src.models import PeriodModel


async def create_period(async_session: async_sessionmaker[AsyncSession], payload: dict):
    async with async_session() as session:
        item_db = PeriodModel(**payload)
        session.add(item_db)
        await session.commit()
        await session.refresh(item_db)
        return item_db


async def get_period_interval(
    async_session: async_sessionmaker[AsyncSession],
    period_name_min: str,
    period_name_max: str,
):
    async with async_session() as session:
        q = await session.execute(
            select(PeriodModel).filter(
                PeriodModel.period_name.between(period_name_min, period_name_max)
            )
        )
        result = q.scalars().all()
        return result


async def create_period_interval(
    async_session: async_sessionmaker[AsyncSession], payload: list[dict]
):
    async with async_session() as session:
        for p in payload:
            item_dict = {"period_code": uuid.uuid4(), "period_name": p}
            item_db = PeriodModel(**item_dict)
            session.add(item_db)
        await session.commit()
        return None

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


async def create_period(async_session: async_sessionmaker[AsyncSession], payload: dict):
    async with async_session() as session:
        item_db=PeriodModel(**payload)
        session.add(item_db)
        await session.commit()
        await session.refresh(item_db)
        return item_db

async def get_period_by_name(async_session: async_sessionmaker[AsyncSession], period_name: str):
    async with async_session() as session:
        q = await session.execute(select(PeriodModel).where(PeriodModel.period_name == period_name))
        return q.scalars().first()

async def get_period_all(async_session: async_sessionmaker[AsyncSession], skip: int, limit: int):
    async with async_session() as session:
        q = await session.execute(select(PeriodModel))
        result = q.scalars().all()
        return result[skip:limit+skip]
    
    

async def main():
    await init_db()
    session = await get_session()
    payload={"period_code":uuid.uuid4(),"period_name":"2024-04-10"}
#    x=await create_period(session, payload)
#    x=await get_period_by_name(session, "2024-04-10")
#    print (x.period_code,x.period_name)
    x=await get_period_all(session,0,10)
    print (x)
asyncio.run(main())

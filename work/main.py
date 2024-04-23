import uuid
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from src.database import init_db, get_session
from src.models import Period


async def create_moteur(
    async_session: async_sessionmaker[AsyncSession], period_name: str
):
    item_db = Period(period_code=uuid.uuid4(), period_name=period_name)
    async with async_session() as session:
        async with session.begin():
            session.add(item_db)
            return item_db


async def main():
    await init_db()
    session = await get_session()

    await create_moteur(session, "2024-04-05")


asyncio.run(main())

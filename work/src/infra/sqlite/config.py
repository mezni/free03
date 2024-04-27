from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.infra.sqlite.base import Base
from src.infra.sqlite.models.provider import ProviderModel


async def init_db(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def create_db_engine(db_url):
    engine = create_async_engine(db_url, echo=True, future=True)
    return engine

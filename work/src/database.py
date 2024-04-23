from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker
from src import models

DATABASE_URL = "sqlite+aiosqlite:///_usage.db"
engine = create_async_engine(DATABASE_URL, echo=True, future=True)


Base = declarative_base()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


async def get_session():
    return async_sessionmaker(engine, expire_on_commit=False)

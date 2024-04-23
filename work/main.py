import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src import models

DATABASE_URL = f"sqlite+aiosqlite:///_usage.db"
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

Base = declarative_base()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
        # await conn.run_sync(SQLModel.metadata.drop_all)


#        await conn.run_sync(SQLModel.metadata.create_all)


async def main():
    await init_db()


asyncio.run(main())

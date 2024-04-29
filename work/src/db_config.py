from sqlalchemy.ext.asyncio import create_async_engine


from src.db_base import Base


async def init_db(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def create_db_engine(db_url):
    engine = create_async_engine(db_url, echo=True, future=True)
    return engine

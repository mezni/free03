import asyncio

from src.infra.sqlite.config import create_db_engine, init_db


async def main():
    db_url = "sqlite+aiosqlite:///_usage.db"
    engine = await create_db_engine(db_url)
    await init_db(engine)


asyncio.run(main())

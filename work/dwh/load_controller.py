import asyncio
from db_config import init_db, create_db_engine


async def execute():
    db_url = "sqlite+aiosqlite:///_store/_dwh.db"
    engine = await create_db_engine(db_url)
    await init_db(engine)




asyncio.run(execute())

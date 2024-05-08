import uuid
import asyncio



async def main():
    db_url = "sqlite+aiosqlite:///_costs.db"
    engine = await create_db_engine(db_url)
    await init_db(engine)



asyncio.run(main())

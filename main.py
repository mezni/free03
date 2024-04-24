import uuid
import asyncio


from src.database import init_db, get_session



async def main():
    await init_db()
    session = await get_session()




asyncio.run(main())

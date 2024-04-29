
import asyncio


async def main():
    db_url = "sqlite+aiosqlite:///_costs.db"
    DATA_SOURCE = "csv"


asyncio.run(main())

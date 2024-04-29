
import asyncio


async def main():
    db_url = "sqlite+aiosqlite:///_costs.db"
    DATA_SOURCE = "csv" # List


asyncio.run(main())

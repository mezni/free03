
import asyncio

async def main():
    db_url = "sqlite+aiosqlite:///_data.db"
    sql_adapter = SQLiteDatabaseAdapter(db_url)

asyncio.run(main())

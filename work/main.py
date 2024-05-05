import asyncio
from src.infra.adapters.sqlite_database_adapter import SQLiteDatabaseAdapter


async def main():
    db_url = "sqlite+aiosqlite:///_data.db"
    sql_adapter = SQLiteDatabaseAdapter(db_url)
    await sql_adapter.init_db()


asyncio.run(main())

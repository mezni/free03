import uuid
import asyncio


from src.database import init_db, get_session
from src.repositories import CreatePeriodDTO
from src.repositories import SQLitePeriodRepository


async def main():
    await init_db()
    session = await get_session()
    period_repo = SQLitePeriodRepository(session)
    period_dto = CreatePeriodDTO("2024-04-01")
    await period_repo.create_period(period_dto)


asyncio.run(main())

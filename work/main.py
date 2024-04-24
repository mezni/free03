import asyncio
from src.database import init_db, get_session
from src.repositories import SQLitePeriodRepository
from src.schemas import PeriodSchemaIn


async def main():
    print("# Enter")
    await init_db()
    session = await get_session()
    period_repo = SQLitePeriodRepository(session)
    x = await period_repo.create_period(PeriodSchemaIn(period_name="2024-04-22"))
    print(x.model_dump())


asyncio.run(main())

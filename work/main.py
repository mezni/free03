import uuid
import asyncio


from src.database import init_db, get_session
from src.repositories import create_period, get_period_interval, create_period_interval


async def main():
    await init_db()
    session = await get_session()
    period_list = ["2024-04-10", "2024-04-04", "2024-04-01"]

    #    payload = {"period_code": uuid.uuid4(), "period_name": "2024-04-10"}
    #    x=await create_period(session, payload)

    x = await create_period_interval(session, period_list)
    x = await get_period_interval(session, "2024-04-01", "2024-04-30")
    print(len(x))
    for a in x:
        print(a.period_code, a.period_name)


asyncio.run(main())

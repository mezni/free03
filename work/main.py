import asyncio
from src.usecases import CreatePeriodInterval


async def main():
    print("# Enter")
    period_interval_repo = None
    create_period_interval_usecase = CreatePeriodInterval(period_interval_repo)
    period_interval_input = ["2024-04-24", "2024-04-10"]
    period_interval_output = await create_period_interval_usecase.execute(
        period_interval_input
    )


asyncio.run(main())

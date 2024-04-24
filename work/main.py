import asyncio
from src.usecases import CreatePeriodInterval


async def main():
    print("# Enter")
    period_interval_repo = None
    create_period_interval_usecase = CreatePeriodInterval(period_interval_repo)
    period_interval_input = []
    period_interval_output = create_period_interval_usecase.execute(
        period_interval_input
    )


asyncio.run(main())

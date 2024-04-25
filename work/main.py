import asyncio
from src.entities import Period
from src.dtos import PeriodInputDTO


async def main():
    #    period_output = PeriodInputDTO(period_name="2024-04-25")
    #    print(period_output.model_dump())
    periods = []
    usage_data = []
    periods_list = ["2024-04-21", "2024-04-02", "2024-04-22"]
    for period in periods_list:
        period_output = PeriodInputDTO(period_name=period)
        period = Period(**period_output.model_dump())
        periods.append(period)
    print(periods)


asyncio.run(main())

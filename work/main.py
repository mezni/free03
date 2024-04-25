import asyncio
from src.dtos import PeriodInputDTO


async def main():
    x = PeriodInputDTO(period_name="2024-04-25")
    print(x.model_dump())


asyncio.run(main())

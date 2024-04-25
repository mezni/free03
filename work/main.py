import asyncio
from src.usecases import LoadUsageUseCase


async def main():
    print("# Enter")
    usage_data = ["2024-04-25", "2024-04-10", "2024-04-11x"]
    repos = None
    load_usage_usecase = LoadUsageUseCase(repos)
    await load_usage_usecase.process(usage_data)


asyncio.run(main())

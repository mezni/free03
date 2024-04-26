import asyncio

from src.infra.in_memory_repositories import InMemoryProviderRepository


async def main():
    repo = InMemoryProviderRepository()


asyncio.run(main())

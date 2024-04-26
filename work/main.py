import asyncio

from src.infra.logger import Logger
from src.app.in_memory_controller import CreateProviderController


async def main():
    """In Memory controller"""
    data = []
    logger = Logger()
    controller = CreateProviderController(logger)
    await controller.execute(data)


asyncio.run(main())

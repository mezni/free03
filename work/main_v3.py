import asyncio
import logging
import sys

import logging


class LoggerDefault:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        handler.setFormatter(
            logging.Formatter(
                fmt="%(asctime)-s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )
        self.logger.addHandler(handler)

    def log_info(self, message: str) -> None:
        self.logger.warning(message)


async def main():
    logger = LoggerDefault()
    logger.log_info("DD")


asyncio.run(main())

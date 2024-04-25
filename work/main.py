import asyncio


class MemCliProcessHandler:
    """Memomy Client Process Handler"""

    def __init__(self) -> None:
        pass

    def execute(self, usage_data) -> None:
        """
        Execute the ProcessHandler

        Args:
            usage_data ([str]): list of periods
        Returns:
            None
        """
        print("# process")


async def main():

    usage_data = ["2024-04-12", "2024-04-12", "2024-04-22"]


asyncio.run(main())

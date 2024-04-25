import asyncio
from datetime import datetime


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


class PeriodIntervalValidator:
    @staticmethod
    def validate_period_interval(periods):
        for period in periods:
            try:
                datetime.strptime(period, "%Y-%m-%d")
            except ValueError as e:
                raise ValueError(f"Bad format '{period}'") from e


class PeriodIntervalController:
    def __init__(self, period_intervals_use_case):
        self.period_intervals_use_case = period_intervals_use_case

    def process_periods(self):
        return None


async def main():
    period_intervals_use_case = None
    period_intervals_controller = PeriodIntervalController(period_intervals_use_case)
    periods = ["2024-04-12", "2024-04-12", "2024-04-22"]
    PeriodIntervalValidator.validate_period_interval(periods)
    processed_periods = period_intervals_controller.process_periods()


asyncio.run(main())

from datetime import datetime, timedelta


class LoadUsageUseCase:
    def __init__(self, repos):
        self.repos = repos

    @classmethod
    async def __validate_period_name(cls, period_name: str) -> str:
        try:
            datetime.strptime(period_name, "%Y-%m-%d")
        except ValueError as e:
            raise ValueError(f"Bad format '{period_name}'") from e

    async def __get_min_max(self, period_list):
        error = None
        period_interval_min = None
        period_interval_max = None
        if len(period_list) != 0:
            period_interval_min = datetime(2200, 1, 1)
            period_interval_max = datetime(1900, 1, 1)
            for p in period_list:
                p_date = datetime.strptime(p, "%Y-%m-%d")
                if p_date < period_interval_min:
                    period_interval_min = p_date
                if p_date > period_interval_max:
                    period_interval_max = p_date
        else:
            error = "Empty imput list"
        return (period_interval_min, period_interval_max), error

    async def __generate_dates(self, min_max):
        periods_list = []
        start_date = min_max[0]
        end_date = min_max[1]
        delta = timedelta(days=1)
        while start_date <= end_date:
            periods_list.append(start_date.strftime("%Y-%m-%d"))
            start_date += delta
        return periods_list

    async def process(self, usage_data):
        for u in usage_data:
            try:
                await self.__validate_period_name(u)
            except Exception as e:
                raise ValueError(f"Bad format '{u}'") from e

            period_interval_min_max, error = await self.__get_min_max(usage_data)
            if not error:
                periods_list = await self.__generate_dates(period_interval_min_max)
                print(periods_list)

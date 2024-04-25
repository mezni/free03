from datetime import datetime, timedelta


class CreatePeriodInterval:
    def __init__(self, period_interval_repo):
        self.period_interval_repo = period_interval_repo

    async def _get_min_max(self, period_list):
        error = None
        period_interval_min = None
        period_interval_max = None
        if len(period_list) != 0:
            period_interval_min = datetime(2200, 1, 1)
            period_interval_max = datetime(1900, 1, 1)
            for p in period_list:
                try:
                    p_date = datetime.strptime(p, "%Y-%m-%d")
                    if p_date < period_interval_min:
                        period_interval_min = p_date
                    if p_date > period_interval_max:
                        period_interval_max = p_date
                except AttributeError:
                    period_interval_min = None
                    period_interval_max = None
                    error = "Element bad format"
                    break
        else:
            error = "Empty imput list"
        return (period_interval_min, period_interval_max), error

    async def _generate_dates(self, min_max):
        periods_list = []
        start_date = min_max[0]
        end_date = min_max[1]
        delta = timedelta(days=1)
        while start_date <= end_date:
            periods_list.append(start_date.strftime("%Y-%m-%d"))
            start_date += delta
        return periods_list

    async def execute(self, period_list):
        min_max, err = await self._get_min_max(period_list)
        if not err:
            periods_list = await self._generate_dates(min_max)
            print(periods_list)


#            period_interval_repo.create_period_interval(periods_list)


class GetAllPeriodInterval:
    def __init__(self, period_interval_repo):
        self.period_interval_repo = period_interval_repo

    def execute(self):
        pass

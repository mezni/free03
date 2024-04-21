from src.domain.entities.period import Period
from src.interactor.directories.period_repo_interface import PeriodRepositoryInterface


class InMemoryPeriodRepository(PeriodRepositoryInterface):
    def __init__(self):
        self._periods = []

    def get_periods_interval(self):
        return self._periods

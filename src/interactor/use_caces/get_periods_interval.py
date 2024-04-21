from typing import List
from src.domain.entities.period import Period
from src.interactor.directories.period_repo_interface import PeriodRepositoryInterface


class GetPeriodsIntervalUseCase:
    def __init__(self, period_repo: PeriodRepositoryInterface):
        self.period_repo = period_repo

    def execute(self) -> List[Period]:
        return self.period_repo.get_periods_interval()

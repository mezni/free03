# usecases.py
import uuid
from datetime import datetime
from src.entities import Period
from src.repositories import PeriodRepositoryInterface


class PeriodLoad:
    def __init__(self, period_repository: PeriodRepositoryInterface):
        self.period_repository = period_repository

    def execute(self, period_name:str):
        period_record=Period(uuid.uuid4(), "2024-04-22")
        self.period_repository.create_period(period_name)
import sqlite3
from src.entities import Period
from src.repositories import PeriodRepositoryInterface


class SQLitePeriodRepository(PeriodRepositoryInterface):
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def create_period(self, period_name: str) -> Period:
        pass

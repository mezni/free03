import uuid
import sqlite3
from abc import ABC, abstractmethod
from typing import List


# Domain Entities
class Period:
    def __init__(self, period_code, period_name):
        self.period_code = period_code
        self.period_name = period_name


# Repositories
class PeriodRepository(ABC):
    @abstractmethod
    def create_period(self, period_code: uuid.UUID, period_name: str) -> Period:
        pass

    @abstractmethod
    def get_period_by_code(self, period_code: uuid.UUID) -> Period:
        pass

    @abstractmethod
    def get_all_periods(self) -> List[Period]:
        pass


class InMemoryPeriodRepository(PeriodRepository):
    def __init__(self):
        self.periods = []

    def create_period(self, period_code: uuid.UUID, period_name: str) -> Period:
        period = Period(period_code, period_name)
        self.periods.append(period)
        return period

    def get_period_by_code(self, period_code: uuid.UUID) -> Period:
        period_ret = None
        for p in self.periods:
            if p.period_code == period_code:
                period_ret = p
        return period_ret

    def get_all_periods(self) -> List[Period]:
        return self.periods


# Use Cases
class PeriodInteractor:
    def __init__(self, period_repository: PeriodRepository):
        self.period_repository = period_repository

    def create_period(self, period_code: uuid.UUID, period_name: str) -> Period:
        return self.period_repository.create_period(period_code, period_name)

    #    def get_user_by_id(self, user_id: int) -> User:
    #       return self.user_repository.get_user_by_id(user_id)

    def get_all_periods(self) -> List[Period]:
        return self.period_repository.get_all_periods()


# Database initialization
def initialize_database():
    conn = sqlite3.connect("_usage.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS periods (
            period_code UUID PRIMARY KEY,
            period_name TEXT
        )
    """
    )
    conn.commit()
    conn.close()


# Example usage
if __name__ == "__main__":
    initialize_database()
    period_repository = InMemoryPeriodRepository()
    period_interactor = PeriodInteractor(period_repository)

    # Create a period
    period = period_interactor.create_period(uuid.uuid4(), "2024-02-02")
    print("period created:", period.period_code, period.period_name)

    # Create a period
    period = period_interactor.create_period(uuid.uuid4(), "2024-02-03")
    print("period created:", period.period_code, period.period_name)

    all_periods = period_interactor.get_all_periods()
    print("All Periods:")
    for period in all_periods:
        print(period.period_code, period.period_name)

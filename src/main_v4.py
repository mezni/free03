import uuid
import dataclasses


# Entities Layer
@dataclasses.dataclass
class Period:
    def __init__(self, period_code, period):
        self.period_code = period_code
        self.period = period

    @classmethod
    def from_dict(self, d):
        return self(**d)

    def to_dict(self):
        return dataclasses.asdict(self)


# DAO Layer
class PeriodDAO:
    def __init__(self):
        print(f"Init PeriodDAO")

    def save(self, period):
        # Simulated database save operation
        print(f"Saving post '{period.period_code} - {period.period}' to database")


# Interfaces/Adapters Layer
class PeriodRepository:
    def __init__(self, entries=None):
        print(f"Init PeriodRepository")
        self.connection = connection

    #        self._entries = []
    #        if entries:
    #            self._entries.extend(entries)

    def add_period(self, period):
        p = Period(uuid.uuid4(), period)
        self._entries.extend(p)


# Use Cases Layer
class UsageLoaderInteractor:
    def __init__(self, period_dao):
        print(f"Init UsageLoaderInteractor")
        self.period_dao = period_dao

    def create_period(self, period):
        period_code = uuid.uuid4()
        p = Period(period_code, period)
        self.period_dao.save(p)
        return p


# Database Layer
import sqlite3


class SqliteDB:
    def __init__(self, db_file):
        print(f"Init SqliteDB")
        self.connection = sqlite3.connect(db_file)
        self.create_tables()

    def create_tables(self):
        cursor = self.connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS periods (
                period_code UUID PRIMARY KEY,
                period TEXT
            )
        """
        )
        self.connection.commit()

    def close(self):
        self.connection.close()


if __name__ == "__main__":
    db = SqliteDB("_demo.db")
    period_repo = PeriodRepository(db.connection)
    period_dao = PeriodDAO()
    period_interactor = UsageLoaderInteractor(period_dao)
    p = period_interactor.create_period("2024-04-01")
    print(p.period_code, p.period)

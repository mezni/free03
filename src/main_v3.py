import uuid


# Entities Layer
class Period:
    def __init__(self, period_code, period):
        self.period_code = period_code
        self.period = period


# Database Layer
import sqlite3


class Database:
    def __init__(self, db_file):
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
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS resources (
                resource_code UUID PRIMARY KEY,
                resource_id TEXT,
                resource_name TEXT
            )
        """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS usages (
                usage_code UUID PRIMARY KEY,
                resource_code UUID,
                period_code UUID,
                usage_amount FLOAT,
                usage_currency TEXT,
                FOREIGN KEY (period_code) REFERENCES periods(period_code),
                FOREIGN KEY (resource_code) REFERENCES resources(resource_code)
            )
        """
        )
        self.connection.commit()

    def close(self):
        self.connection.close()


# Interfaces/Adapters Layer
class PeriodRepository:
    def __init__(self, connection):
        self.connection = connection

    def add(self, period):
        cursor = self.connection.cursor()
        period_code = str(uuid.uuid4())
        cursor.execute("INSERT INTO periods VALUES (?,?)", (period_code, period))
        self.connection.commit()

    def get_by_code(self, period_code):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM periods WHERE period_code=?", (period_code,))
        row = cursor.fetchone()
        if row:
            return Period(row[0], row[1])
        return None

    def get_all(self):
        periods = []
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM periods")
        result = cursor.fetchall()
        for row in result:
            periods.append(Period(row[0], row[1]))
        return periods


# Database Layer
db = Database("_demo.db")
period_repo = PeriodRepository(db.connection)

period_repo.add("2024-04-01")
for period in period_repo.get_all():
    print(f"  Period={period.period_code} - {period.period}")

x = period_repo.get_by_code("7d6b7171-2be2-48f0-a51c-2de02901e627")
print(f"  Period={x.period_code} - {x.period}")

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


# Database Layer
import sqlite3


class SqliteDB:
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
        self.connection.commit()

    def close(self):
        self.connection.close()


# DAO Layer
class PeriodDAO:
    def __init__(self, connection):
        self.connection = connection

    def add(self, period):
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO periods (period_code, period) VALUES (?, ?)",
            (period.period_code, period.period),
        )
        self.connection.commit()

    def list(self):
        period_list = []
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM periods")
        result = cursor.fetchall()
        for row in result:
            p = Period(row[0], row[1])
            period_list.append(p)
        return period_list


if __name__ == "__main__":
    db = SqliteDB("_demo.db")
    period_dao = PeriodDAO(db.connection)
    p1 = Period(str(uuid.uuid4()), "2024-04-01")
    p2 = Period(str(uuid.uuid4()), "2024-04-02")
    period_dao.add(p1)
    period_dao.add(p2)
    pl = period_dao.list()
    for i in pl:
        print(i.period_code, i.period)

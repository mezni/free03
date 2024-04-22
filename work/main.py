import uuid
from src.entities import Period
from src.sqlitedb import SQLitePeriodRepository
from src.usecases import PeriodLoad



def main():
    period_repository = SQLitePeriodRepository("demo.db")
    period_usecase = PeriodLoad(period_repository)
    period_usecase.execute("2024-04-22")

main()
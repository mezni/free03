from sqlalchemy import (
    UUID,
    Column,
    String,
    Date,
    Boolean,
    Integer,
)


from sqlalchemy.orm import declarative_base

Base = declarative_base()


class PeriodModel(Base):
    __tablename__ = "periods"
    period_code = Column(UUID, primary_key=True, index=True)
    period_name = Column(String(60), unique=True, nullable=False, index=True)
    period_date = Column(Date, unique=True, nullable=False)
    period_day = Column(Integer, nullable=False)
    period_month = Column(Integer, nullable=False)
    period_year = Column(Integer, nullable=False)
    period_is_holiday = Column(Boolean, nullable=False)

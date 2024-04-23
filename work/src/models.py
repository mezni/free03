# import uuid
# from datetime import datetime, time

from sqlalchemy import (
    UUID,
    Column,
    String,
)  # TIMESTAMP, Column, ForeignKey, String, Integer, Float, Boolean, text, Date, Time, Sequence, Identity, UUID

# from sqlalchemy.orm import relationship


from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Period(Base):
    __tablename__ = "periods"
    period_code = Column(UUID, primary_key=True, index=True)
    period_name = Column(String(60), unique=True, nullable=False, index=True)


#    period_date = Column(Date, unique=True, nullable=False)

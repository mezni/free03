from sqlalchemy.orm import Session, sessionmaker

from src.db.engine import engine

SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    autoflush=False,
    autocommit=False,
)

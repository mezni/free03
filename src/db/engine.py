from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from src.config.settings import get_settings


def create_database_engine() -> Engine:
    """Create the SQLAlchemy database engine."""
    settings = get_settings()

    return create_engine(
        settings.database_url,
        pool_pre_ping=True,
    )


engine = create_database_engine()

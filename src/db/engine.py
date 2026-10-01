from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from src.config.settings import get_settings


def create_database_engine() -> Engine:
    """Create the SQLAlchemy database engine.

    Pool settings are read from production configuration.
    ``pool_pre_ping=True`` detects stale connections.
    """
    settings = get_settings()

    return create_engine(
        settings.database_url,
        pool_size=settings.production.database.pool_size,
        max_overflow=settings.production.database.max_overflow,
        pool_timeout=settings.production.database.pool_timeout_seconds,
        pool_recycle=settings.production.database.pool_recycle_seconds,
        pool_pre_ping=True,
    )


engine = create_database_engine()
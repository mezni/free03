from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from src.application.container import ApplicationContainer
from src.config.settings import get_settings
from src.db.session import SessionLocal
from src.services.rag_service import RAGService


def get_db_session() -> Generator[Session]:
    session = SessionLocal()

    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_rag_service(
    session: Session = Depends(get_db_session),
) -> RAGService:
    settings = get_settings()

    container = ApplicationContainer(
        session=session,
        settings=settings,
    )

    return container.rag_service()
from sqlalchemy import select

from src.core.enums import DocumentProcessingOperation
from src.db.models.document_processing import DocumentProcessingDB
from src.services.document_processing_service import (
    DocumentProcessingService,
)
from src.services.ingestion_run_service import IngestionRunService


def test_record_success(database_session):
    run_service = IngestionRunService(database_session)
    processing_service = DocumentProcessingService(database_session)

    run = run_service.start("ingestion")

    record = processing_service.record_success(
        run_id=run.id,
        source_uri="data/raw/test.md",
        operation=DocumentProcessingOperation.ADD,
    )

    assert record.id is not None
    assert record.run_id == run.id
    assert record.operation == "add"
    assert record.status == "success"


def test_processing_record_is_committed(
    database_session,
):
    run_service = IngestionRunService(database_session)
    processing_service = DocumentProcessingService(database_session)

    run = run_service.start("ingestion")

    processing_service.record_success(
        run_id=run.id,
        source_uri="data/raw/test.md",
        operation=DocumentProcessingOperation.ADD,
    )

    database_session.rollback()

    statement = select(DocumentProcessingDB).where(DocumentProcessingDB.run_id == run.id)

    records = list(database_session.execute(statement).scalars().all())

    assert len(records) == 1
    assert records[0].status == "success"

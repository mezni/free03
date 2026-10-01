from src.core.enums import (
    DocumentChangeType,
    DocumentLifecycleStatus,
    DocumentProcessingStatus,
    IngestionRunStatus,
)


def test_document_change_types():
    assert DocumentChangeType.NEW.value == "new"
    assert DocumentChangeType.MODIFIED.value == "modified"
    assert DocumentChangeType.UNCHANGED.value == "unchanged"


def test_document_lifecycle_statuses():
    assert DocumentLifecycleStatus.PENDING.value == "pending"
    assert DocumentLifecycleStatus.PROCESSING.value == "processing"
    assert DocumentLifecycleStatus.ACTIVE.value == "active"
    assert DocumentLifecycleStatus.FAILED.value == "failed"
    assert DocumentLifecycleStatus.DELETED.value == "deleted"


def test_ingestion_run_statuses():
    assert IngestionRunStatus.RUNNING.value == "running"
    assert IngestionRunStatus.COMPLETED.value == "completed"
    assert IngestionRunStatus.FAILED.value == "failed"


def test_document_processing_statuses():
    assert DocumentProcessingStatus.SUCCESS.value == "success"
    assert DocumentProcessingStatus.SKIPPED.value == "skipped"
    assert DocumentProcessingStatus.FAILED.value == "failed"

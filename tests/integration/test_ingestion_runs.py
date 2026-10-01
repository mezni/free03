from src.services.ingestion_run_service import IngestionRunService


def test_create_ingestion_run(database_session):
    service = IngestionRunService(database_session)

    run = service.start("ingestion")

    assert run.id is not None
    assert run.run_type == "ingestion"
    assert run.status == "running"


def test_complete_ingestion_run(database_session):
    service = IngestionRunService(database_session)

    run = service.start("ingestion")
    completed = service.complete(run.id)

    assert completed.status == "completed"
    assert completed.completed_at is not None


def test_fail_ingestion_run(database_session):
    service = IngestionRunService(database_session)

    run = service.start("ingestion")
    failed = service.fail(
        run.id,
        "Test failure",
    )

    assert failed.status == "failed"
    assert failed.error_message == "Test failure"
    assert failed.completed_at is not None

from uuid import UUID

from sqlalchemy.orm import Session

from src.db.repositories.runs import IngestionRunRepository


class IngestionRunService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.repository = IngestionRunRepository(session)

    def start(self, run_type: str):
        run = self.repository.create(run_type)

        self.session.commit()

        return run

    def complete(self, run_id: UUID):
        run = self.repository.get_by_id(run_id)

        if run is None:
            raise ValueError(f"Ingestion run not found: {run_id}")

        self.repository.mark_completed(run)
        self.session.commit()

        return run

    def fail(
        self,
        run_id: UUID,
        error_message: str,
    ):
        run = self.repository.get_by_id(run_id)

        if run is None:
            raise ValueError(f"Ingestion run not found: {run_id}")

        self.repository.mark_failed(
            run,
            error_message,
        )

        self.session.commit()

        return run

    def update_counts(
        self,
        run_id: UUID,
        *,
        discovered_count: int | None = None,
        processed_count: int | None = None,
        skipped_count: int | None = None,
        failed_count: int | None = None,
    ):
        run = self.repository.get_by_id(run_id)

        if run is None:
            raise ValueError(f"Ingestion run not found: {run_id}")

        self.repository.update_counts(
            run,
            discovered_count=discovered_count,
            processed_count=processed_count,
            skipped_count=skipped_count,
            failed_count=failed_count,
        )

        self.session.commit()

        return run

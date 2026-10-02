"""CLI entry point for the ingestion worker.

Run with: uv run python -m src.cli.worker
"""

import argparse

from src.application.container import ApplicationContainer
from src.config.settings import get_settings
from src.db.session import SessionLocal
from src.workers.ingestion_worker import IngestionWorker


def main() -> None:
    parser = argparse.ArgumentParser(
        description="RAG System Ingestion Worker"
    )
    parser.add_argument(
        "--sleep",
        type=float,
        default=1.0,
        help="Sleep seconds between checks for pending jobs",
    )
    args = parser.parse_args()

    settings = get_settings()
    session = SessionLocal()

    container = ApplicationContainer(
        session=session,
        settings=settings,
    )

    # Get services from container
    job_repository = container.ingestion_job_repository()
    job_service = container.ingestion_job_service()
    ingestion_service = container.ingestion_service()
    worker = IngestionWorker(
        job_repository=job_repository,
        job_service=job_service,
        ingestion_service=ingestion_service,
    )

    print("Ingestion worker started...")
    worker.run_loop(sleep_seconds=args.sleep)


if __name__ == "__main__":
    main()
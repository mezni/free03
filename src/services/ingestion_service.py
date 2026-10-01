from src.ingestion.pipeline import IngestionPipeline


class IngestionService:
    """Product/application use case for document ingestion.

    Wraps the technical IngestionPipeline to provide a clean product
    operation boundary. This separation becomes useful when the API later
    needs authorization, audit events, asynchronous execution, job tracking,
    quotas, and notifications.
    """

    def __init__(self, pipeline: IngestionPipeline) -> None:
        self._pipeline = pipeline

    def ingest(self):
        return self._pipeline.run()
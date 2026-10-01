from src.ingestion.context import DocumentChange, RawDocument
from src.ingestion.loaders.base import DocumentLoader
from src.ingestion.stages.base import PipelineStage


class LoadStage(PipelineStage[DocumentChange, RawDocument]):
    """Load raw content for a changed document."""

    def __init__(self, loader: DocumentLoader) -> None:
        self.loader = loader

    def execute(
        self,
        data: DocumentChange,
    ) -> RawDocument:
        return self.loader.load(
            document=data.document,
            content_hash=data.content_hash,
        )

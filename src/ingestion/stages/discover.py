from src.ingestion.context import DocumentInput
from src.ingestion.sources.base import DocumentSource
from src.ingestion.stages.base import PipelineStage


class DiscoveryStage(PipelineStage[None, list[DocumentInput]]):
    """Discover documents from an ingestion source."""

    def __init__(self, source: DocumentSource) -> None:
        self.source = source

    def execute(self, data: None = None) -> list[DocumentInput]:
        return self.source.discover()

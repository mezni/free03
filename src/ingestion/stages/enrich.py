from src.ingestion.context import CleanedDocument, EnrichedDocument
from src.ingestion.metadata import MetadataExtractor
from src.ingestion.stages.base import PipelineStage


class EnrichStage(PipelineStage[CleanedDocument, EnrichedDocument]):
    """Extract metadata and enrich a cleaned document."""

    def __init__(self, extractor: MetadataExtractor) -> None:
        self.extractor = extractor

    def execute(self, data: CleanedDocument) -> EnrichedDocument:
        metadata = self.extractor.extract(data)

        return EnrichedDocument(
            document=data.document,
            content=data.content,
            content_hash=data.content_hash,
            format=data.format,
            metadata=metadata,
        )

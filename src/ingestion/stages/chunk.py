from src.ingestion.chunking import DocumentChunker
from src.ingestion.context import ChunkedDocument, EnrichedDocument
from src.ingestion.stages.base import PipelineStage


class ChunkStage(PipelineStage[EnrichedDocument, ChunkedDocument]):
    """Split an enriched document into chunks."""

    def __init__(self, chunker: DocumentChunker) -> None:
        self.chunker = chunker

    def execute(self, data: EnrichedDocument) -> ChunkedDocument:
        chunks = self.chunker.chunk(data)

        return ChunkedDocument(
            document=data.document,
            content_hash=data.content_hash,
            metadata=data.metadata,
            chunks=chunks,
        )

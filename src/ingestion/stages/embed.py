from src.ingestion.context import (
    ChunkedDocument,
    ChunkEmbedding,
    EmbeddedDocument,
)
from src.ingestion.stages.base import PipelineStage
from src.providers.embeddings.base import EmbeddingProvider


class EmbedStage(PipelineStage[ChunkedDocument, EmbeddedDocument]):
    """Generate embeddings for document chunks."""

    def __init__(self, provider: EmbeddingProvider) -> None:
        self.provider = provider

    def execute(self, data: ChunkedDocument) -> EmbeddedDocument:
        texts = [
            chunk.content
            for chunk in data.chunks
        ]

        vectors = self.provider.embed(texts)

        if len(vectors) != len(data.chunks):
            raise ValueError(
                "Embedding provider returned an unexpected number of vectors"
            )

        embeddings = [
            ChunkEmbedding(
                chunk_id=chunk.chunk_id,
                vector=vector,
                model_name=self.provider.model_name,
                dimensions=self.provider.dimensions,
            )
            for chunk, vector in zip(data.chunks, vectors, strict=True)
        ]

        return EmbeddedDocument(
            document=data.document,
            content_hash=data.content_hash,
            metadata=data.metadata,
            chunks=data.chunks,
            embeddings=embeddings,
        )
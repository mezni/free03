from src.ingestion.chunking import DocumentChunker
from src.ingestion.context import DocumentChunk, EnrichedDocument


class CharacterTextChunker(DocumentChunker):
    """Split documents into fixed-size character chunks."""

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
    ) -> None:
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than zero")

        if chunk_overlap < 0:
            raise ValueError("chunk_overlap cannot be negative")

        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size")

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk(self, document: EnrichedDocument) -> list[DocumentChunk]:
        content = document.content

        if not content:
            return []

        chunks: list[DocumentChunk] = []

        start = 0
        chunk_index = 0
        step = self.chunk_size - self.chunk_overlap

        while start < len(content):
            end = min(start + self.chunk_size, len(content))

            chunk_content = content[start:end]

            chunks.append(
                DocumentChunk(
                    chunk_id=f"{document.content_hash[:16]}-{chunk_index}",
                    document=document.document,
                    content=chunk_content,
                    content_hash=document.content_hash,
                    chunk_index=chunk_index,
                    start_char=start,
                    end_char=end,
                    metadata=document.metadata,
                )
            )

            if end == len(content):
                break

            start += step
            chunk_index += 1

        return chunks

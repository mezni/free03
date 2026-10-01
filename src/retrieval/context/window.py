from src.db.repositories.chunks import ChunkRepository
from src.models.retrieval import RetrievalResult


class ContextWindowService:
    """Expand each retrieved chunk to its neighbors in the same document.

    Answers often span adjacent chunks: retrieving chunk 11 alone can
    miss the context that makes chunk 12 understandable.

    Database access stays in the repository. This service receives the
    data it needs rather than issuing queries itself, so retrieval
    policy stays testable without a database.
    """

    def __init__(
        self,
        chunk_repository: ChunkRepository,
    ) -> None:
        self._chunk_repository = chunk_repository

    def expand(
        self,
        results: list[RetrievalResult],
        window: int = 1,
    ) -> list[RetrievalResult]:
        if window <= 0:
            return list(results)

        expanded: list[RetrievalResult] = []
        seen: set[str] = set()

        for result in results:
            chunks = (
                self._chunk_repository.get_neighboring_chunks(
                    document_id=result.document_id,
                    index_version_id=result.index_version_id,
                    chunk_index=result.chunk_index,
                    window=window,
                )
            )

            for chunk in chunks:
                chunk_id = str(chunk.id)

                if chunk_id in seen:
                    continue

                seen.add(chunk_id)

                expanded.append(
                    RetrievalResult(
                        chunk_id=chunk.id,
                        document_id=chunk.document_id,
                        index_version_id=chunk.index_version_id,
                        content=chunk.content,
                        chunk_index=chunk.chunk_index,
                        # Neighbors inherit the score of the chunk that
                        # pulled them in: their own relevance was never
                        # measured by the search.
                        score=result.score,
                        retrieval_method="context_window",
                    )
                )

        return expanded
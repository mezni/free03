from uuid import UUID, uuid4

from src.models.retrieval import RetrievalResult
from src.retrieval.context.window import ContextWindowService


class FakeChunk:
    """Stands in for a ChunkDB row."""

    def __init__(
        self,
        id: UUID,
        document_id: UUID,
        index_version_id: UUID,
        chunk_index: int,
        content: str,
    ) -> None:
        self.id = id
        self.document_id = document_id
        self.index_version_id = index_version_id
        self.chunk_index = chunk_index
        self.content = content


class FakeChunkRepository:
    """Records the arguments of each window lookup."""

    def __init__(self, chunks: dict[UUID, list[FakeChunk]]) -> None:
        self.chunks = chunks
        self.calls: list[dict] = []

    def get_neighboring_chunks(
        self,
        document_id,
        index_version_id,
        chunk_index,
        window=1,
    ) -> list[FakeChunk]:
        self.calls.append(
            {
                "document_id": document_id,
                "index_version_id": index_version_id,
                "chunk_index": chunk_index,
                "window": window,
            }
        )

        if document_id not in self.chunks:
            return []

        return [
            chunk
            for chunk in self.chunks[document_id]
            if chunk.index_version_id == index_version_id
            and chunk.chunk_index >= chunk_index - window
            and chunk.chunk_index <= chunk_index + window
        ]


def build_document(
    index_version_id: UUID,
    count: int = 5,
) -> tuple[UUID, list[FakeChunk]]:
    document_id = uuid4()

    chunks = [
        FakeChunk(
            id=uuid4(),
            document_id=document_id,
            index_version_id=index_version_id,
            chunk_index=index,
            content=f"chunk {index} content",
        )
        for index in range(count)
    ]

    return document_id, chunks


def make_result(
    chunk: FakeChunk,
    score: float = 0.9,
) -> RetrievalResult:
    return RetrievalResult(
        chunk_id=chunk.id,
        document_id=chunk.document_id,
        index_version_id=chunk.index_version_id,
        content=chunk.content,
        chunk_index=chunk.chunk_index,
        score=score,
        retrieval_method="vector",
    )


def test_window_expands_to_neighbors() -> None:
    version_id = uuid4()
    document_id, chunks = build_document(version_id)

    repository = FakeChunkRepository({document_id: chunks})
    service = ContextWindowService(repository)

    expanded = service.expand(
        [make_result(chunks[2])],
        window=1,
    )

    assert [r.chunk_index for r in expanded] == [1, 2, 3]
    assert all(
        r.index_version_id == version_id
        for r in expanded
    )


def test_window_of_zero_returns_results_unchanged() -> None:
    version_id = uuid4()
    document_id, chunks = build_document(version_id)

    repository = FakeChunkRepository({document_id: chunks})
    service = ContextWindowService(repository)

    results = [make_result(chunks[2])]

    assert service.expand(results, window=0) == results
    assert repository.calls == []


def test_window_deduplicates_overlapping_expansions() -> None:
    version_id = uuid4()
    document_id, chunks = build_document(version_id)

    repository = FakeChunkRepository({document_id: chunks})
    service = ContextWindowService(repository)

    expanded = service.expand(
        [make_result(chunks[1]), make_result(chunks[2])],
        window=1,
    )

    indexes = [r.chunk_index for r in expanded]

    assert indexes == [0, 1, 2, 3]
    assert len(indexes) == len(set(indexes))


def test_window_never_crosses_index_versions() -> None:
    """The invariant this whole phase protects.

    Two versions of the same document can share chunk indexes. A
    window lookup that omitted index_version_id would mix them.
    """
    active_version = uuid4()
    retired_version = uuid4()

    document_id = uuid4()

    active_chunks = [
        FakeChunk(
            id=uuid4(),
            document_id=document_id,
            index_version_id=active_version,
            chunk_index=index,
            content=f"v3 chunk {index}",
        )
        for index in range(3)
    ]

    retired_chunks = [
        FakeChunk(
            id=uuid4(),
            document_id=document_id,
            index_version_id=retired_version,
            chunk_index=index,
            content=f"v2 chunk {index}",
        )
        for index in range(3)
    ]

    repository = FakeChunkRepository(
        {document_id: [*active_chunks, *retired_chunks]}
    )

    service = ContextWindowService(repository)

    expanded = service.expand(
        [make_result(active_chunks[1])],
        window=1,
    )

    assert {r.index_version_id for r in expanded} == {
        active_version
    }
    assert all(
        r.content.startswith("v3")
        for r in expanded
    )
    assert repository.calls[0]["index_version_id"] == active_version


def test_window_passes_version_on_every_lookup() -> None:
    version_id = uuid4()
    document_id, chunks = build_document(version_id)

    repository = FakeChunkRepository({document_id: chunks})
    service = ContextWindowService(repository)

    service.expand(
        [make_result(chunks[0]), make_result(chunks[3])],
        window=1,
    )

    assert len(repository.calls) == 2
    assert all(
        call["index_version_id"] == version_id
        for call in repository.calls
    )
    assert all(
        call["window"] == 1
        for call in repository.calls
    )


def test_window_preserves_retrieved_score() -> None:
    """Neighbors inherit the score of the chunk that pulled them in.

    Their own relevance was never measured by search.
    """
    version_id = uuid4()
    document_id, chunks = build_document(version_id)

    repository = FakeChunkRepository({document_id: chunks})
    service = ContextWindowService(repository)

    expanded = service.expand(
        [make_result(chunks[1], score=0.42)],
        window=1,
    )

    assert [r.score for r in expanded] == [0.42, 0.42, 0.42]
    assert all(
        r.retrieval_method == "context_window"
        for r in expanded
    )


def test_window_returns_empty_for_no_results() -> None:
    service = ContextWindowService(
        FakeChunkRepository({})
    )

    assert service.expand([], window=1) == []
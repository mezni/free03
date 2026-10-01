from uuid import uuid4

import pytest

from src.models.retrieval_evaluation import (
    EvaluationChunkReference,
)
from src.services.evaluation_resolver import EvaluationResolver

DOCUMENT_URI = "data/raw/billing/sample-policy.md"


class FakeIndexVersion:
    def __init__(self, version_number=1):
        self.id = uuid4()
        self.version_number = version_number


class FakeIndexVersionRepository:
    def __init__(self, version=None):
        self.version = version

    def get_active(self):
        return self.version


class FakeDocument:
    def __init__(self, document_id, source_uri):
        self.id = document_id
        self.source_uri = source_uri


class FakeDocumentRepository:
    def __init__(self, documents):
        self.documents = documents

    def get_by_source_uri(self, source_uri):
        return self.documents.get(source_uri)


class FakeChunk:
    def __init__(self, chunk_id, chunk_index):
        self.id = chunk_id
        self.chunk_index = chunk_index


class FakeChunkRepository:
    def __init__(self, chunks):
        self.chunks = chunks

    def get_by_document_id_and_version(
        self,
        document_id,
        index_version_id,
    ):
        return self.chunks.get(
            (document_id, index_version_id),
            [],
        )


def make_resolver():
    version = FakeIndexVersion()

    document_id = uuid4()
    chunk_id = uuid4()

    document = FakeDocument(
        document_id=document_id,
        source_uri=DOCUMENT_URI,
    )

    chunk_repository = FakeChunkRepository(
        {
            (document_id, version.id): [
                FakeChunk(chunk_id=chunk_id, chunk_index=2),
            ],
        }
    )

    resolver = EvaluationResolver(
        document_repository=FakeDocumentRepository(
            {
                document.source_uri: document,
            }
        ),
        chunk_repository=chunk_repository,
        index_version_repository=FakeIndexVersionRepository(
            version
        ),
    )

    return resolver, version, document_id, chunk_repository, chunk_id


def test_resolve_chunk():
    resolver, _, _, _, expected_chunk_id = make_resolver()

    reference = EvaluationChunkReference(
        document=DOCUMENT_URI,
        chunk_index=2,
    )

    result = resolver.resolve(reference)

    assert result == expected_chunk_id


def test_resolve_missing_document():
    resolver, _, _, _, _ = make_resolver()

    reference = EvaluationChunkReference(
        document="does-not-exist.md",
        chunk_index=0,
    )

    with pytest.raises(
        LookupError,
        match="Evaluation document not found",
    ):
        resolver.resolve(reference)


def test_resolve_missing_chunk():
    resolver, _, _, _, _ = make_resolver()

    reference = EvaluationChunkReference(
        document=DOCUMENT_URI,
        chunk_index=99,
    )

    with pytest.raises(
        LookupError,
        match="Evaluation chunk not found",
    ):
        resolver.resolve(reference)


def test_resolve_requires_active_index():
    resolver = EvaluationResolver(
        document_repository=FakeDocumentRepository({}),
        chunk_repository=FakeChunkRepository({}),
        index_version_repository=FakeIndexVersionRepository(None),
    )

    reference = EvaluationChunkReference(
        document=DOCUMENT_URI,
        chunk_index=0,
    )

    with pytest.raises(
        RuntimeError,
        match="No active index version exists",
    ):
        resolver.resolve(reference)


def test_resolve_all():
    resolver, version, document_id, chunk_repository, first = (
        make_resolver()
    )

    second_chunk_id = uuid4()

    chunk_repository.chunks[(document_id, version.id)].append(
        FakeChunk(chunk_id=second_chunk_id, chunk_index=3)
    )

    references = [
        EvaluationChunkReference(
            document=DOCUMENT_URI,
            chunk_index=2,
        ),
        EvaluationChunkReference(
            document=DOCUMENT_URI,
            chunk_index=3,
        ),
    ]

    result = resolver.resolve_all(references)

    assert result == [first, second_chunk_id]


def test_resolve_all_empty():
    resolver, _, _, _, _ = make_resolver()

    assert resolver.resolve_all([]) == []


def test_resolve_all_preserves_input_order():
    resolver, version, document_id, chunk_repository, target = (
        make_resolver()
    )

    first_chunk = FakeChunk(chunk_id=uuid4(), chunk_index=0)

    chunk_repository.chunks[(document_id, version.id)] = [
        first_chunk,
        FakeChunk(chunk_id=target, chunk_index=2),
    ]

    references = [
        EvaluationChunkReference(
            document=DOCUMENT_URI,
            chunk_index=2,
        ),
        EvaluationChunkReference(
            document=DOCUMENT_URI,
            chunk_index=0,
        ),
    ]

    result = resolver.resolve_all(references)

    assert result == [target, first_chunk.id]


def test_resolve_ignores_chunks_from_other_versions():
    resolver, version, document_id, chunk_repository, _ = (
        make_resolver()
    )

    other_version_chunk = FakeChunk(
        chunk_id=uuid4(),
        chunk_index=2,
    )

    chunk_repository.chunks[
        (document_id, uuid4())
    ] = [other_version_chunk]

    reference = EvaluationChunkReference(
        document=DOCUMENT_URI,
        chunk_index=2,
    )

    result = resolver.resolve(reference)

    assert result != other_version_chunk.id
    assert result == chunk_repository.chunks[
        (document_id, version.id)
    ][0].id
from uuid import uuid4

from src.generation.citations import CitationExtractor
from src.models.retrieval import RetrievalResult


def make_results(count: int) -> list[RetrievalResult]:
    return [
        RetrievalResult(
            chunk_id=uuid4(),
            document_id=uuid4(),
            index_version_id=uuid4(),
            content=f"content {index}",
            chunk_index=index,
            score=0.5,
            retrieval_method="vector",
        )
        for index in range(count)
    ]


def test_single_citation():
    results = make_results(1)

    citations = CitationExtractor().extract(
        answer="Disputes are filed within 30 days. [SOURCE-1]",
        results=results,
    )

    assert len(citations) == 1
    assert citations[0].citation_id == "SOURCE-1"
    assert citations[0].chunk_id == str(results[0].chunk_id)
    assert citations[0].document_id == str(results[0].document_id)
    assert citations[0].chunk_index == 0


def test_two_citations():
    results = make_results(2)

    citations = CitationExtractor().extract(
        answer="A [SOURCE-1] and B [SOURCE-2]",
        results=results,
    )

    assert len(citations) == 2

    assert citations[0].citation_id == "SOURCE-1"
    assert citations[1].citation_id == "SOURCE-2"


def test_invalid_source_number_is_ignored():
    results = make_results(1)

    citations = CitationExtractor().extract(
        answer="Nothing here. [SOURCE-99]",
        results=results,
    )

    assert citations == []


def test_duplicate_citation_is_deduplicated():
    results = make_results(2)

    citations = CitationExtractor().extract(
        answer="A [SOURCE-1] again [SOURCE-1]",
        results=results,
    )

    assert len(citations) == 1


def test_answer_without_citation_yields_no_citations():
    results = make_results(2)

    citations = CitationExtractor().extract(
        answer="No markers at all.",
        results=results,
    )

    assert citations == []


def test_citations_follow_first_appearance_order():
    results = make_results(3)

    citations = CitationExtractor().extract(
        answer="Second [SOURCE-2] then first [SOURCE-1]",
        results=results,
    )

    assert [c.citation_id for c in citations] == [
        "SOURCE-2",
        "SOURCE-1",
    ]

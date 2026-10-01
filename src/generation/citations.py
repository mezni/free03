import re

from src.models.rag import Citation
from src.models.retrieval import RetrievalResult


class CitationExtractor:
    """Map [SOURCE-N] markers in an answer back to retrieved chunks."""

    _PATTERN = re.compile(r"\[SOURCE-(\d+)\]")

    def extract(
        self,
        answer: str,
        results: list[RetrievalResult],
    ) -> list[Citation]:
        citations: list[Citation] = []
        seen: set[int] = set()

        for match in self._PATTERN.finditer(answer):
            source_number = int(match.group(1))

            if source_number in seen:
                continue

            index = source_number - 1

            if index < 0 or index >= len(results):
                continue

            result = results[index]

            citations.append(
                Citation(
                    citation_id=f"SOURCE-{source_number}",
                    document_id=str(result.document_id),
                    chunk_id=str(result.chunk_id),
                    chunk_index=result.chunk_index,
                )
            )

            seen.add(source_number)

        return citations

from src.models.retrieval import RetrievalResult


class ContextBuilder:
    """Render retrieved chunks into a cited source context."""

    def build(
        self,
        results: list[RetrievalResult],
    ) -> str:
        sections: list[str] = []

        for position, result in enumerate(results, start=1):
            section = (
                f"[SOURCE-{position}]\n"
                f"Document ID: {result.document_id}\n"
                f"Chunk ID: {result.chunk_id}\n"
                f"Chunk Index: {result.chunk_index}\n"
                f"Content:\n{result.content}"
            )

            sections.append(section)

        return "\n\n".join(sections)
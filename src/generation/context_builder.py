from src.models.retrieval import RetrievalResult


class ContextBuilder:
    """Build a grounded prompt context from retrieved chunks."""

    def build(
        self,
        results: list[RetrievalResult],
    ) -> str:
        if not results:
            return ""

        sections = []

        for result in results:
            sections.append(
                
                    f"[Document: {result.document_id} | "
                    f"Chunk: {result.chunk_index}]\n"
                    f"{result.content}"
                
            )

        return "\n\n".join(sections)
from src.models.rag import RAGResponse
from src.models.retrieval import RetrievalQuery
from src.retrieval.pipeline import RetrievalPipeline
from src.services.generation_service import GenerationService


class RAGService:
    """Retrieve relevant context, then generate a grounded answer."""

    def __init__(
        self,
        retrieval_pipeline: RetrievalPipeline,
        generation_service: GenerationService,
    ) -> None:
        self._retrieval_pipeline = retrieval_pipeline
        self._generation_service = generation_service

    def answer(
        self,
        query: RetrievalQuery,
    ) -> RAGResponse:
        results = self._retrieval_pipeline.execute(query)

        return self._generation_service.generate(
            query=query.query,
            results=results,
        )

from fastapi import APIRouter, Depends

from src.api.dependencies import get_rag_service
from src.models.api import RAGQueryRequest, RAGQueryResponse
from src.models.retrieval import RetrievalQuery
from src.services.rag_service import RAGService

router = APIRouter(
    prefix="/rag",
    tags=["rag"],
)


@router.post(
    "/query",
    response_model=RAGQueryResponse,
)
def query_rag(
    request: RAGQueryRequest,
    rag_service: RAGService = Depends(get_rag_service),
) -> RAGQueryResponse:
    retrieval_query = RetrievalQuery(
        query=request.query,
        top_k=request.top_k,
    )

    response = rag_service.answer(
        retrieval_query,
    )

    return RAGQueryResponse(
        query=response.query,
        answer=response.answer,
        citations=response.citations,
        model_name=response.model_name,
        retrieved_count=response.retrieved_count,
    )

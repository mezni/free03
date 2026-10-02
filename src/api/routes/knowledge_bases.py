from fastapi import APIRouter, Depends, HTTPException

from src.api.dependencies import get_knowledge_base_service
from src.models.knowledge_base import KnowledgeBase
from src.services.knowledge_base_service import KnowledgeBaseService

router = APIRouter(prefix="/knowledge-bases", tags=["knowledge-bases"])


@router.post("/", response_model=KnowledgeBase)
def create_knowledge_base(
    name: str,
    slug: str,
    description: str | None = None,
    service: KnowledgeBaseService = Depends(get_knowledge_base_service),
):
    return service.create_knowledge_base(name=name, slug=slug, description=description)


@router.get("/", response_model=list[KnowledgeBase])
def list_knowledge_bases(
    service: KnowledgeBaseService = Depends(get_knowledge_base_service),
):
    return service.list_knowledge_bases()


@router.get("/{kb_id}", response_model=KnowledgeBase)
def get_knowledge_base(
    kb_id: UUID,
    service: KnowledgeBaseService = Depends(get_knowledge_base_service),
):
    kb = service.get_knowledge_base(kb_id)
    if kb is None:
        raise HTTPException(status_code=404, detail="Knowledge base not found")
    return kb


@router.delete("/{kb_id}")
def delete_knowledge_base(
    kb_id: UUID,
    service: KnowledgeBaseService = Depends(get_knowledge_base_service),
):
    result = service.delete_knowledge_base(kb_id)
    if result["status"] == "error":
        raise HTTPException(status_code=409, detail=result["message"])
    return {"detail": result["message"]}
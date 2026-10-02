from uuid import UUID

from src.db.repositories.knowledge_bases import KnowledgeBaseRepository
from src.models.knowledge_base import KnowledgeBase


class KnowledgeBaseService:
    def __init__(self, repository: KnowledgeBaseRepository):
        self.repository = repository

    def create_knowledge_base(self, name: str, slug: str, description: str | None = None) -> KnowledgeBase:
        kb = self.repository.create(name=name, slug=slug, description=description)
        return KnowledgeBase(
            id=kb.id,
            name=kb.name,
            slug=kb.slug,
            description=kb.description,
            created_at=kb.created_at,
            updated_at=kb.updated_at,
        )

    def get_knowledge_base(self, kb_id: UUID) -> KnowledgeBase | None:
        kb = self.repository.get_by_id(kb_id)
        if kb is None:
            return None
        return KnowledgeBase(
            id=kb.id,
            name=kb.name,
            slug=kb.slug,
            description=kb.description,
            created_at=kb.created_at,
            updated_at=kb.updated_at,
        )

    def list_knowledge_bases(self) -> list[KnowledgeBase]:
        kbs = self.repository.list()
        return [
            KnowledgeBase(
                id=kb.id,
                name=kb.name,
                slug=kb.slug,
                description=kb.description,
                created_at=kb.created_at,
                updated_at=kb.updated_at,
            )
            for kb in kbs
        ]

    def delete_knowledge_base(self, kb_id: UUID) -> dict:
        """Delete a knowledge base. Returns dict with status and message."""
        success = self.repository.delete(kb_id)
        if success:
            return {"status": "success", "message": "Knowledge base deleted."}
        else:
            return {"status": "error", "message": "The knowledge base cannot be deleted"}
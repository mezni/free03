from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from src.db.models.document import DocumentDB
from src.db.models.knowledge_base import KnowledgeBaseDB


class KnowledgeBaseRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, name: str, slug: str, description: str | None = None) -> KnowledgeBaseDB:
        kb = KnowledgeBaseDB(
            name=name,
            slug=slug,
            description=description,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        self.session.add(kb)
        self.session.commit()
        self.session.refresh(kb)
        return kb

    def get_by_id(self, kb_id: UUID) -> KnowledgeBaseDB | None:
        stmt = select(KnowledgeBaseDB).where(KnowledgeBaseDB.id == kb_id)
        result = self.session.execute(stmt)
        return result.scalar_one_or_none()

    def get_by_slug(self, slug: str) -> KnowledgeBaseDB | None:
        stmt = select(KnowledgeBaseDB).where(KnowledgeBaseDB.slug == slug)
        result = self.session.execute(stmt)
        return result.scalar_one_or_none()

    def list(self) -> list[KnowledgeBaseDB]:
        stmt = select(KnowledgeBaseDB).order_by(KnowledgeBaseDB.created_at.desc())
        result = self.session.execute(stmt)
        return list(result.scalars().all())

    def delete(self, kb_id: UUID) -> bool:
        """Delete a knowledge base. Returns True if successful, False if not empty."""
        # Check if documents belong to this knowledge base
        stmt = select(DocumentDB).where(DocumentDB.knowledge_base_id == kb_id)
        result = self.session.execute(stmt)
        documents = result.scalars().all()

        if documents:
            return False  # Cannot delete non-empty KB

        stmt = delete(KnowledgeBaseDB).where(KnowledgeBaseDB.id == kb_id)
        self.session.execute(stmt)
        self.session.commit()
        return True
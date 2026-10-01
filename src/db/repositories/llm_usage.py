from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.db.models.llm_usage import LLMUsageDB
from src.models.llm_usage import LLMUsageRecord


class LLMUsageRepository:
    """Persists LLM usage history.

    Transaction ownership stays with the caller: this only flushes.
    """

    def __init__(self, session: Session) -> None:
        self._session = session

    @property
    def session(self) -> Session:
        """Exposed so the calling service can own the transaction."""
        return self._session

    def create(
        self,
        usage: LLMUsageRecord,
    ) -> LLMUsageRecord:
        record = LLMUsageDB(
            request_id=usage.request_id,
            provider=usage.provider,
            model_name=usage.model_name,
            prompt_tokens=usage.prompt_tokens,
            completion_tokens=usage.completion_tokens,
            total_tokens=usage.total_tokens,
            estimated_cost=usage.estimated_cost,
            currency=usage.currency,
        )

        self._session.add(record)
        self._session.flush()

        return LLMUsageRecord(
            id=record.id,
            request_id=record.request_id,
            provider=record.provider,
            model_name=record.model_name,
            prompt_tokens=record.prompt_tokens,
            completion_tokens=record.completion_tokens,
            total_tokens=record.total_tokens,
            estimated_cost=record.estimated_cost,
            currency=record.currency,
            created_at=record.created_at,
        )

    def list_by_request_id(
        self,
        request_id: str,
    ) -> list[LLMUsageRecord]:
        statement = (
            select(LLMUsageDB)
            .where(LLMUsageDB.request_id == request_id)
            .order_by(LLMUsageDB.created_at)
        )

        records = self._session.execute(
            statement
        ).scalars()

        return [self._to_record(record) for record in records]

    def get_by_id(
        self,
        usage_id: UUID,
    ) -> LLMUsageRecord | None:
        statement = select(LLMUsageDB).where(
            LLMUsageDB.id == usage_id
        )

        record = self._session.execute(
            statement
        ).scalar_one_or_none()

        if record is None:
            return None

        return self._to_record(record)

    @staticmethod
    def _to_record(record: LLMUsageDB) -> LLMUsageRecord:
        return LLMUsageRecord(
            id=record.id,
            request_id=record.request_id,
            provider=record.provider,
            model_name=record.model_name,
            prompt_tokens=record.prompt_tokens,
            completion_tokens=record.completion_tokens,
            total_tokens=record.total_tokens,
            estimated_cost=record.estimated_cost,
            currency=record.currency,
            created_at=record.created_at,
        )
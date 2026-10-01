from sqlalchemy import select
from sqlalchemy.orm import Session

from src.db.models.audit import AuditEventDB
from src.models.audit import AuditEvent


class AuditRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(
        self,
        event: AuditEvent,
    ) -> AuditEvent:
        record = AuditEventDB(
            request_id=event.request_id,
            event_type=event.event_type,
            actor=event.actor,
            resource_type=event.resource_type,
            resource_id=event.resource_id,
        )

        self._session.add(record)
        self._session.flush()

        return AuditEvent(
            id=record.id,
            request_id=record.request_id,
            event_type=record.event_type,
            actor=event.actor,
            resource_type=record.resource_type,
            resource_id=record.resource_id,
            created_at=record.created_at,
        )

    def get_by_id(self, event_id) -> AuditEvent | None:
        record = self._session.execute(
            select(AuditEventDB).where(AuditEventDB.id == event_id)
        ).scalar_one_or_none()

        if record is None:
            return None

        return self._to_model(record)

    def list_by_request(
        self,
        request_id: str,
    ) -> list[AuditEvent]:
        records = (
            self._session.execute(
                select(AuditEventDB)
                .where(AuditEventDB.request_id == request_id)
                .order_by(AuditEventDB.created_at)
            )
            .scalars()
            .all()
        )

        return [self._to_model(record) for record in records]

    def _to_model(self, record: AuditEventDB) -> AuditEvent:
        return AuditEvent(
            id=record.id,
            request_id=record.request_id,
            event_type=record.event_type,
            actor=record.actor,
            resource_type=record.resource_type,
            resource_id=record.resource_id,
            created_at=record.created_at,
        )
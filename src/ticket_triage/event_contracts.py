"""The agreed format for events exchanged between components.

An event is data describing something that happened or work that is requested.
It is not executable code. Every event carries an identifier, a type, a schema
version, an occurrence timestamp, and a JSON payload, so producers and consumers
can evolve independently and reject payloads they do not understand.

Two kinds of idempotency matter in this architecture:

- **Message idempotency:** receiving the same event again must not create a
  duplicate logical job. ``event_id`` is the stable key for this.
- **Business-operation idempotency:** repeating the work must not duplicate or
  corrupt business state. This requires state checks or version checks in the
  consumer, not just a unique message ID.
"""

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

CURRENT_SCHEMA_VERSION = 1


@dataclass(frozen=True)
class EventEnvelope:
    event_id: str
    event_type: str
    schema_version: int
    occurred_at: str
    payload: dict[str, Any]

    @classmethod
    def create(
        cls,
        *,
        event_id: str,
        event_type: str,
        payload: dict[str, Any],
    ) -> "EventEnvelope":
        if not event_id.strip():
            raise ValueError("event_id is required.")
        if not event_type.strip():
            raise ValueError("event_type is required.")
        if not isinstance(payload, dict):
            raise ValueError("payload must be an object.")

        return cls(
            event_id=event_id,
            event_type=event_type,
            schema_version=CURRENT_SCHEMA_VERSION,
            occurred_at=datetime.now(UTC).isoformat(),
            payload=payload,
        )

    def to_json(self) -> str:
        return json.dumps(
            {
                "event_id": self.event_id,
                "event_type": self.event_type,
                "schema_version": self.schema_version,
                "occurred_at": self.occurred_at,
                "payload": self.payload,
            }
        )

    @classmethod
    def from_json(cls, raw: str) -> "EventEnvelope":
        try:
            data = json.loads(raw)
        except (TypeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid event JSON.") from exc

        if not isinstance(data, dict):
            raise ValueError("Event must be a JSON object.")

        required = {
            "event_id",
            "event_type",
            "schema_version",
            "occurred_at",
            "payload",
        }
        if set(data) != required:
            raise ValueError("Event fields do not match the contract.")

        if (
            not isinstance(data["event_id"], str)
            or not data["event_id"].strip()
            or not isinstance(data["event_type"], str)
            or not data["event_type"].strip()
            or type(data["schema_version"]) is not int
            or data["schema_version"] != CURRENT_SCHEMA_VERSION
            or not isinstance(data["occurred_at"], str)
            or not isinstance(data["payload"], dict)
        ):
            raise ValueError("Invalid event field values.")

        return cls(**data)

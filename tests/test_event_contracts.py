import pytest

from ticket_triage.event_contracts import EventEnvelope


def test_event_round_trip():
    event = EventEnvelope.create(
        event_id="classify:case-001",
        event_type="classification_requested",
        payload={"case_id": "case-001"},
    )

    restored = EventEnvelope.from_json(event.to_json())

    assert restored.event_id == event.event_id
    assert restored.event_type == event.event_type
    assert restored.schema_version == 1
    assert restored.payload == {"case_id": "case-001"}


def test_invalid_json_is_rejected():
    with pytest.raises(ValueError):
        EventEnvelope.from_json("{invalid")


def test_unknown_schema_version_is_rejected():
    raw = (
        '{"event_id":"e1",'
        '"event_type":"classification_requested",'
        '"schema_version":2,'
        '"occurred_at":"2026-10-11T00:00:00+00:00",'
        '"payload":{"case_id":"case-001"}}'
    )

    with pytest.raises(ValueError):
        EventEnvelope.from_json(raw)


def test_missing_event_fields_are_rejected():
    with pytest.raises(ValueError):
        EventEnvelope.from_json('{"event_id":"e1"}')


def test_extra_event_fields_are_rejected():
    raw = (
        '{"event_id":"e1",'
        '"event_type":"classification_requested",'
        '"schema_version":1,'
        '"occurred_at":"2026-10-11T00:00:00+00:00",'
        '"payload":{"case_id":"case-001"},'
        '"unexpected":true}'
    )

    with pytest.raises(ValueError):
        EventEnvelope.from_json(raw)


def test_non_object_json_is_rejected():
    with pytest.raises(ValueError):
        EventEnvelope.from_json("[1, 2, 3]")


def test_create_requires_event_id_and_type():
    with pytest.raises(ValueError):
        EventEnvelope.create(event_id="", event_type="x", payload={})
    with pytest.raises(ValueError):
        EventEnvelope.create(event_id="e1", event_type=" ", payload={})


def test_create_requires_object_payload():
    with pytest.raises(ValueError):
        EventEnvelope.create(event_id="e1", event_type="x", payload=["not", "a", "map"])


def test_created_event_is_versioned_and_timestamped():
    event = EventEnvelope.create(
        event_id="classify:case-001",
        event_type="classification_requested",
        payload={"case_id": "case-001"},
    )

    assert event.schema_version == 1
    assert event.occurred_at.endswith("+00:00")

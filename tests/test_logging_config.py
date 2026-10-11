import json
import logging

from ticket_triage.logging_config import (
    JsonFormatter,
    correlation_id_var,
    valid_correlation_id,
)


def test_accepts_bounded_correlation_id():
    assert valid_correlation_id("request-123")
    assert valid_correlation_id("trace_abc.42")


def test_rejects_invalid_correlation_id():
    assert not valid_correlation_id(None)
    assert not valid_correlation_id("")
    assert not valid_correlation_id("contains spaces")
    assert not valid_correlation_id("x" * 101)
    assert not valid_correlation_id("request\nforged-log-entry")


def test_json_formatter_includes_correlation_id():
    token = correlation_id_var.set("test-correlation-1")

    try:
        record = logging.LogRecord(
            name="ticket_triage.test",
            level=logging.INFO,
            pathname=__file__,
            lineno=10,
            msg="classification_completed",
            args=(),
            exc_info=None,
        )
        record.event = "classification_completed"
        record.case_id = "case-1"

        output = JsonFormatter().format(record)
        payload = json.loads(output)

        assert payload["message"] == "classification_completed"
        assert payload["event"] == "classification_completed"
        assert payload["case_id"] == "case-1"
        assert payload["correlation_id"] == "test-correlation-1"
        assert payload["level"] == "INFO"
        assert "timestamp" in payload
    finally:
        correlation_id_var.reset(token)

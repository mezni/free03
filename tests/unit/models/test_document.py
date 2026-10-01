import pytest
from pydantic import ValidationError

from src.core.enums import DocumentLifecycleStatus
from src.models.document import DocumentCreate


def test_document_create():
    document = DocumentCreate(
        source="filesystem",
        source_uri="data/raw/billing/sample.md",
        title="Billing Policy",
        content_hash="a" * 64,
    )

    assert document.source == "filesystem"
    assert document.title == "Billing Policy"


def test_document_rejects_invalid_hash():
    with pytest.raises(ValidationError):
        DocumentCreate(
            source="filesystem",
            source_uri="data/raw/billing/sample.md",
            content_hash="invalid",
        )


def test_document_status_defaults_to_pending():
    document = DocumentCreate(
        source="filesystem",
        source_uri="data/raw/billing/sample.md",
        content_hash="a" * 64,
    )

    assert document.status == DocumentLifecycleStatus.PENDING

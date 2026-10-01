from pathlib import Path

from src.core.enums import DocumentChangeType
from src.ingestion.change_detection import ChangeDetector
from src.ingestion.context import DocumentInput


def test_new_document(tmp_path: Path):
    document_path = tmp_path / "policy.md"

    document_path.write_text(
        "# Billing Policy",
        encoding="utf-8",
    )

    document = DocumentInput(
        source="filesystem",
        source_uri=str(document_path),
        path=document_path,
    )

    detector = ChangeDetector()

    result = detector.detect(
        document=document,
        previous_content_hash=None,
    )

    assert result.change_type == DocumentChangeType.NEW
    assert result.previous_content_hash is None
    assert len(result.content_hash) == 64


def test_unchanged_document(tmp_path: Path):
    document_path = tmp_path / "policy.md"

    document_path.write_text(
        "# Billing Policy",
        encoding="utf-8",
    )

    document = DocumentInput(
        source="filesystem",
        source_uri=str(document_path),
        path=document_path,
    )

    detector = ChangeDetector()

    first_result = detector.detect(
        document=document,
        previous_content_hash=None,
    )

    second_result = detector.detect(
        document=document,
        previous_content_hash=first_result.content_hash,
    )

    assert second_result.change_type == DocumentChangeType.UNCHANGED
    assert second_result.content_hash == first_result.content_hash


def test_modified_document(tmp_path: Path):
    document_path = tmp_path / "policy.md"

    document_path.write_text(
        "# Billing Policy",
        encoding="utf-8",
    )

    document = DocumentInput(
        source="filesystem",
        source_uri=str(document_path),
        path=document_path,
    )

    detector = ChangeDetector()

    first_result = detector.detect(
        document=document,
        previous_content_hash=None,
    )

    document_path.write_text(
        "# Updated Billing Policy",
        encoding="utf-8",
    )

    second_result = detector.detect(
        document=document,
        previous_content_hash=first_result.content_hash,
    )

    assert second_result.change_type == DocumentChangeType.MODIFIED

    assert second_result.content_hash != first_result.content_hash

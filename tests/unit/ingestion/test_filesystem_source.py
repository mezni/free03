from pathlib import Path

from src.ingestion.sources.filesystem import FilesystemSource


def test_filesystem_source_discovers_markdown_files(tmp_path: Path):
    billing_dir = tmp_path / "billing"
    billing_dir.mkdir()

    document = billing_dir / "policy.md"
    document.write_text(
        "# Billing Policy\n\nCustomers are billed monthly.",
        encoding="utf-8",
    )

    source = FilesystemSource(tmp_path)

    documents = source.discover()

    assert len(documents) == 1
    assert documents[0].source == "filesystem"
    assert documents[0].path == document
    assert documents[0].source_uri == str(document)

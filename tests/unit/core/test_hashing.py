from pathlib import Path

from src.core.hashing import calculate_file_hash


def test_calculate_file_hash(tmp_path: Path):
    document = tmp_path / "document.txt"

    document.write_text(
        "Hello RAG",
        encoding="utf-8",
    )

    first_hash = calculate_file_hash(document)
    second_hash = calculate_file_hash(document)

    assert first_hash == second_hash
    assert len(first_hash) == 64

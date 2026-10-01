from pathlib import Path

import pytest

from src.evaluation.dataset_loader import (
    RetrievalEvaluationDatasetLoader,
)


def test_load_evaluation_dataset(tmp_path: Path):
    dataset_path = tmp_path / "retrieval.yaml"

    dataset_path.write_text(
        """
version: 1

cases:
  - case_id: billing-001
    query: "What is the billing policy?"
    relevant_chunks:
      - document: "data/raw/billing/sample-policy.md"
        chunk_index: 0
""",
        encoding="utf-8",
    )

    loader = RetrievalEvaluationDatasetLoader()

    dataset = loader.load(dataset_path)

    assert dataset.version == 1
    assert len(dataset.cases) == 1
    assert dataset.cases[0].case_id == "billing-001"
    assert dataset.cases[0].query == "What is the billing policy?"
    assert dataset.cases[0].relevant_chunks[0].document == (
        "data/raw/billing/sample-policy.md"
    )
    assert dataset.cases[0].relevant_chunks[0].chunk_index == 0


def test_load_missing_dataset():
    loader = RetrievalEvaluationDatasetLoader()

    with pytest.raises(
        FileNotFoundError,
        match="Evaluation dataset not found",
    ):
        loader.load("/does/not/exist/retrieval.yaml")


def test_load_invalid_dataset(tmp_path: Path):
    dataset_path = tmp_path / "invalid.yaml"

    dataset_path.write_text(
        """
version: 1

cases:
  - case_id: billing-001
    query: "What is the billing policy?"
    relevant_chunks: []
""",
        encoding="utf-8",
    )

    loader = RetrievalEvaluationDatasetLoader()

    with pytest.raises(ValueError):
        loader.load(dataset_path)


def test_load_dataset_root_not_a_mapping(tmp_path: Path):
    dataset_path = tmp_path / "list.yaml"

    dataset_path.write_text(
        "- case_id: billing-001\n",
        encoding="utf-8",
    )

    loader = RetrievalEvaluationDatasetLoader()

    with pytest.raises(
        ValueError,
        match="Evaluation dataset root must be a mapping",
    ):
        loader.load(dataset_path)


def test_load_empty_dataset_rejected(tmp_path: Path):
    dataset_path = tmp_path / "empty.yaml"

    dataset_path.write_text(
        "version: 1\ncases: []\n",
        encoding="utf-8",
    )

    loader = RetrievalEvaluationDatasetLoader()

    with pytest.raises(ValueError):
        loader.load(dataset_path)


def test_load_unknown_field_rejected(tmp_path: Path):
    dataset_path = tmp_path / "extra.yaml"

    dataset_path.write_text(
        """
version: 1
author: someone

cases:
  - case_id: billing-001
    query: "What is the billing policy?"
    relevant_chunks:
      - document: "data/raw/billing/sample-policy.md"
        chunk_index: 0
""",
        encoding="utf-8",
    )

    loader = RetrievalEvaluationDatasetLoader()

    with pytest.raises(ValueError):
        loader.load(dataset_path)


def test_load_repository_dataset():
    loader = RetrievalEvaluationDatasetLoader()

    dataset = loader.load(
        "data/evaluation/retrieval_v1.yaml",
    )

    assert dataset.version == 1
    assert len(dataset.cases) == 3
    assert dataset.cases[0].case_id == "billing-policy-001"
    assert dataset.cases[0].relevant_chunks[0].document == (
        "data/raw/billing/sample-policy.md"
    )
    assert dataset.cases[0].relevant_chunks[0].chunk_index == 0
    assert dataset.cases[1].relevant_chunks[0].chunk_index == 1
    assert dataset.cases[2].relevant_chunks[0].document == (
        "data/raw/security/account-security.md"
    )
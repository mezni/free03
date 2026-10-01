import pytest

from src.evaluation.rag_dataset_loader import (
    RAGEvaluationDatasetLoader,
)


@pytest.fixture
def dataset_path(tmp_path):
    def _write(content: str):
        path = tmp_path / "rag_v1.yaml"
        path.write_text(content, encoding="utf-8")

        return path

    return _write


class TestRAGEvaluationDatasetLoader:
    def test_loads_version_and_cases(
        self,
        dataset_path,
    ) -> None:
        path = dataset_path(
            """
version: 1
cases:
  - case_id: billing-policy-answer-001
    query: "What is the billing dispute policy?"
    reference_answer: "Customers can dispute billing charges."
    expected_citations:
      - SOURCE-1
"""
        )

        version, cases = RAGEvaluationDatasetLoader().load(path)

        assert version == 1
        assert len(cases) == 1
        assert cases[0].case_id == "billing-policy-answer-001"
        assert cases[0].expected_citations == ["SOURCE-1"]

    def test_accepts_string_path(self, dataset_path) -> None:
        path = dataset_path(
            """
version: 2
cases:
  - case_id: case-001
    query: "q"
    reference_answer: "a"
"""
        )

        version, cases = RAGEvaluationDatasetLoader().load(str(path))

        assert version == 2
        assert cases[0].expected_citations == []

    def test_shipped_dataset_loads(self) -> None:
        version, cases = RAGEvaluationDatasetLoader().load("data/evaluation/rag_v1.yaml")

        assert version == 1
        assert len(cases) == 3

    def test_missing_file_raises(self) -> None:
        with pytest.raises(
            FileNotFoundError,
            match="Evaluation dataset not found",
        ):
            RAGEvaluationDatasetLoader().load("data/evaluation/does-not-exist.yaml")

    def test_non_mapping_root_raises(self, dataset_path) -> None:
        path = dataset_path("- just\n- a list\n")

        with pytest.raises(
            ValueError,
            match="root must be a mapping",
        ):
            RAGEvaluationDatasetLoader().load(path)

    def test_non_integer_version_raises(self, dataset_path) -> None:
        path = dataset_path(
            "version: one\ncases:\n  - case_id: c\n    query: q\n    reference_answer: a\n"
        )

        with pytest.raises(
            ValueError,
            match="version must be an integer",
        ):
            RAGEvaluationDatasetLoader().load(path)

    def test_non_list_cases_raises(self, dataset_path) -> None:
        path = dataset_path("version: 1\ncases:\n  case_id: c\n")

        with pytest.raises(
            ValueError,
            match="cases must be a list",
        ):
            RAGEvaluationDatasetLoader().load(path)

    def test_empty_case_list_raises(self, dataset_path) -> None:
        path = dataset_path("version: 1\ncases: []\n")

        with pytest.raises(
            ValueError,
            match="at least one case",
        ):
            RAGEvaluationDatasetLoader().load(path)

    def test_invalid_case_fails_validation(
        self,
        dataset_path,
    ) -> None:
        path = dataset_path(
            """
version: 1
cases:
  - case_id: ""
    query: "q"
    reference_answer: "a"
"""
        )

        with pytest.raises(ValueError):
            RAGEvaluationDatasetLoader().load(path)

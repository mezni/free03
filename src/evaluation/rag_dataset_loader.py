from pathlib import Path

import yaml

from src.models.rag_evaluation import RAGEvaluationCase


class RAGEvaluationDatasetLoader:
    def load(
        self,
        path: str | Path,
    ) -> tuple[int, list[RAGEvaluationCase]]:
        dataset_path = Path(path)

        if not dataset_path.exists():
            raise FileNotFoundError(
                f"Evaluation dataset not found: {dataset_path}"
            )

        with dataset_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            data = yaml.safe_load(file)

        if not isinstance(data, dict):
            raise ValueError(
                "Evaluation dataset root must be a mapping."
            )

        version = data.get("version")

        if not isinstance(version, int):
            raise ValueError(
                "Evaluation dataset version must be an integer."
            )

        raw_cases = data.get("cases")

        if not isinstance(raw_cases, list):
            raise ValueError(
                "Evaluation dataset cases must be a list."
            )

        cases = [
            RAGEvaluationCase.model_validate(case)
            for case in raw_cases
        ]

        if not cases:
            raise ValueError(
                "Evaluation dataset must contain at least one case."
            )

        return version, cases
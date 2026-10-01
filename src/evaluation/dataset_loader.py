from pathlib import Path

import yaml

from src.models.retrieval_evaluation_dataset import (
    RetrievalEvaluationDataset,
)


class RetrievalEvaluationDatasetLoader:
    """Load and validate retrieval evaluation datasets."""

    def load(
        self,
        path: str | Path,
    ) -> RetrievalEvaluationDataset:
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

        return RetrievalEvaluationDataset.model_validate(data)
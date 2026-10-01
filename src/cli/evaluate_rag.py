import argparse

from src.application.container import ApplicationContainer
from src.config.settings import get_settings
from src.db.session import SessionLocal
from src.evaluation.rag_dataset_loader import (
    RAGEvaluationDatasetLoader,
)
from src.evaluation.rag_evaluation_runner import (
    RAGEvaluationRunner,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run RAG evaluation."
    )

    parser.add_argument(
        "--dataset",
        default="data/evaluation/rag_v1.yaml",
    )

    args = parser.parse_args()

    settings = get_settings()

    with SessionLocal() as session:
        container = ApplicationContainer(
            session=session,
            settings=settings,
        )

        runner = RAGEvaluationRunner(
            dataset_loader=RAGEvaluationDatasetLoader(),
            evaluation_service=(
                container.rag_evaluation_service()
            ),
        )

        version, metrics = runner.run(
            args.dataset
        )

    print()
    print("RAG Evaluation")
    print("================")
    print(f"Dataset version: {version}")
    print()
    print(
        f"Answer relevance:    "
        f"{metrics.answer_relevance:.3f}"
    )
    print(
        f"Citation precision:  "
        f"{metrics.citation_precision:.3f}"
    )
    print(
        f"Citation recall:     "
        f"{metrics.citation_recall:.3f}"
    )
    print(
        f"Grounding:           "
        f"{metrics.grounding:.3f}"
    )


if __name__ == "__main__":
    main()
import argparse

from src.application.container import ApplicationContainer
from src.config.settings import get_settings
from src.db.session import SessionLocal
from src.evaluation.dataset_loader import (
    RetrievalEvaluationDatasetLoader,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run retrieval evaluation."
    )

    parser.add_argument(
        "--dataset",
        default="data/evaluation/retrieval_v1.yaml",
    )

    parser.add_argument(
        "--k",
        type=int,
        default=5,
    )

    args = parser.parse_args()

    if args.k <= 0:
        parser.error("--k must be greater than 0")

    settings = get_settings()

    with SessionLocal() as session:
        container = ApplicationContainer(
            session=session,
            settings=settings,
        )

        dataset_loader = RetrievalEvaluationDatasetLoader()

        dataset = dataset_loader.load(args.dataset)

        version = dataset.version
        cases = dataset.cases

        runner = container.retrieval_evaluation_runner()

        metrics = runner.evaluate(
            cases,
            args.k,
        )

    print()
    print("Retrieval Evaluation")
    print("====================")
    print(f"Dataset version: {version}")
    print(f"K: {args.k}")
    print()
    print(f"Recall@{args.k}:           {metrics.recall_at_k:.3f}")
    print(
        f"Precision@{args.k}:        "
        f"{metrics.precision_at_k:.3f}"
    )
    print(f"MRR:                      {metrics.mrr:.3f}")
    print(f"NDCG@{args.k}:             {metrics.ndcg_at_k:.3f}")

    if metrics.context_recall is not None:
        print(
            f"Context recall:           "
            f"{metrics.context_recall:.3f}"
        )
        print(
            f"Context precision:        "
            f"{metrics.context_precision:.3f}"
        )


if __name__ == "__main__":
    main()
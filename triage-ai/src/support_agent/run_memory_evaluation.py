import json
from pathlib import Path

from support_agent.memory_evaluation import (
    evaluate_memory_case,
)


def main():

    cases_path = Path(
        "data/memory_evaluation_cases.json"
    )

    cases = json.loads(
        cases_path.read_text()
    )

    results = []

    for case in cases:

        result = evaluate_memory_case(
            name=case["name"],
            customer_id=case["customer_id"],
            query=case["query"],
            expected_memory_key=case[
                "expected_memory_key"
            ],
        )

        results.append(result)

        print(
            f"{result.status.value.upper():5} "
            f"{result.name}: "
            f"{result.details}"
        )

    passed = sum(
        result.status == EvaluationStatus.PASS
        for result in results
    )

    print()
    print(
        f"Passed: {passed}/{len(results)}"
    )


if __name__ == "__main__":
    main()
from support_agent.data.loader import load_tickets
from support_agent.evaluation import (
    evaluate_case,
    load_evaluation_cases,
)
from support_agent.extraction import extract_ticket
from support_agent.triage import decide_triage


def main():

    tickets = load_tickets(
        "data/tickets/tickets.json"
    )

    cases = load_evaluation_cases(
        "data/evaluation_cases.json"
    )

    tickets_by_id = {
        ticket.ticket_id: ticket
        for ticket in tickets
    }

    results = []

    for case in cases:

        ticket = tickets_by_id[case.ticket_id]

        print("=" * 60)
        print(f"Case: {case.case_id}")
        print(f"Ticket: {case.ticket_id}")

        extraction = extract_ticket(
            ticket
        )

        triage = decide_triage(
            extraction
        )

        result = evaluate_case(
            extraction=extraction,
            triage=triage,
            expected=case,
        )

        results.append(result)

        for name, passed in result.checks.items():

            status = (
                "PASS"
                if passed
                else "FAIL"
            )

            print(
                f"{name:15} {status}"
            )

    passed_cases = sum(
        result.passed
        for result in results
    )

    total_cases = len(results)

    pass_rate = (
        passed_cases / total_cases
        if total_cases
        else 0
    )

    print("\n" + "=" * 60)
    print("Evaluation Summary")
    print("=" * 60)

    print(
        f"Passed: {passed_cases}/{total_cases}"
    )

    print(
        f"Pass rate: {pass_rate:.1%}"
    )


if __name__ == "__main__":
    main()
from support_agent.data.loader import load_tickets
from support_agent.extraction import extract_ticket
from support_agent.triage import decide_triage


def main():
    tickets = load_tickets("data/tickets/tickets.json")

    for ticket in tickets:
        print("=" * 60)
        print(f"Ticket: {ticket.ticket_id}")
        print(f"Subject: {ticket.subject}")

        extraction = extract_ticket(ticket)

        print("\nExtraction:")
        print(f"  Customer ID: {extraction.customer_id}")
        print(f"  Product: {extraction.product}")
        print(f"  Sentiment: {extraction.sentiment}")
        print(f"  Priority: {extraction.priority}")

        decision = decide_triage(extraction)

        print("\nTriage Decision:")
        print(f"  Category: {decision.category}")
        print(f"  Urgency: {decision.urgency}")
        print(
            f"  Knowledge Search: "
            f"{decision.needs_knowledge_search}"
        )
        print(
            f"  Escalation: "
            f"{decision.needs_escalation}"
        )


if __name__ == "__main__":
    main()
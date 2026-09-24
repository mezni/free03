from support_agent.agent import run_agent
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

        triage = decide_triage(extraction)

        print("\nTriage:")
        print(f"  Category: {triage.category}")
        print(f"  Urgency: {triage.urgency}")
        print(
            f"  Knowledge Search: "
            f"{triage.needs_knowledge_search}"
        )
        print(
            f"  Escalation: "
            f"{triage.needs_escalation}"
        )

        response = run_agent(
            user_message=f"""
Subject:
{ticket.subject}

Message:
{ticket.body}
""",
            extraction=extraction,
            triage=triage,
        )

        print("\nAgent Response:")
        print(response)


if __name__ == "__main__":
    main()
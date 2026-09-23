from support_agent.data.loader import load_tickets
from support_agent.extraction import extract_ticket


def main():
    tickets = load_tickets("data/tickets/tickets.json")

    for ticket in tickets:
        print("=" * 60)
        print(f"Ticket: {ticket.ticket_id}")
        print(f"Subject: {ticket.subject}")

        extraction = extract_ticket(ticket)

        print(f"Customer ID: {extraction.customer_id}")
        print(f"Product: {extraction.product}")
        print(f"Sentiment: {extraction.sentiment}")
        print(f"Priority: {extraction.priority}")


if __name__ == "__main__":
    main()
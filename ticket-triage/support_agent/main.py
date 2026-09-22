import json
from pathlib import Path

from support_agent.agent import SupportTicket, triage_ticket


def main() -> None:
    tickets_path = Path("data/tickets.json")

    tickets = json.loads(
        tickets_path.read_text()
    )

    ticket = SupportTicket.model_validate(tickets[0])

    result = triage_ticket(ticket)

    print("Ticket:")
    print(ticket.message)

    print("\nTriage result:")
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
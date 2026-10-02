import json
from pathlib import Path

from triage_ai.models.ticket import SupportTicket


def load_tickets(path: str | Path) -> list[SupportTicket]:
    file_path = Path(path)

    with file_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return [
        SupportTicket.model_validate(ticket)
        for ticket in data
    ]
import json
from pathlib import Path

from support_agent.models.ticket import SupportTicket


def load_tickets(path: str) -> list[SupportTicket]:
    file_path = Path(path)

    with file_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return [
        SupportTicket.model_validate(item)
        for item in data
    ]
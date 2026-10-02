from pathlib import Path

import typer
from rich import print

from triage_ai.config import settings
from triage_ai.data.loader import load_tickets
from support_agent.database import initialize_database


app = typer.Typer()


@app.callback()
def callback() -> None:
    """triage-ai command line interface."""


@app.command()
def info() -> None:
    """Display application information."""
    print(f"[bold]Application:[/bold] {settings.app_name}")
    print(f"[bold]Environment:[/bold] {settings.environment}")
    print(f"[bold]Debug:[/bold] {settings.debug}")


@app.command()
def tickets() -> None:
    """Display the seed support tickets."""
    tickets_path = Path("data/tickets.json")
    support_tickets = load_tickets(tickets_path)

    for ticket in support_tickets:
        print(f"[bold]{ticket.ticket_id}[/bold] - {ticket.subject}")


if __name__ == "__main__":
    initialize_database()
    app()
# triage-ai

AI-powered support ticket triage. A CLI that loads support tickets, classifies
and prioritizes them via an LLM, and drafts responses.

## Features

- **Typer CLI** with Rich output — `info`, `tickets` commands.
- **JSON data ingestion** — `load_tickets()` validates a JSON array into
  `SupportTicket` Pydantic models.
- **Pydantic domain model** — `SupportTicket` (`ticket_id`, `customer_id`,
  `subject`, `description`) with field validation.
- **Settings via pydantic-settings** — `.env` support, OpenRouter config
  (`OPENROUTER_API_KEY`, `OPENROUTER_MODEL`).
- **LLM integration** — `ChatOpenRouter` client factory (LangChain OpenRouter)
  wired to settings, ready for triage prompts.

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) for dependency management

## Setup

```bash
# Install dependencies
uv sync

# Configure environment
cp .env.example .env
# edit .env — set OPENROUTER_API_KEY

# Run the test suite
uv run pytest
```

## Usage

```bash
# Show application info
uv run triage-ai info

# List seed tickets
uv run triage-ai tickets
```

## Project Layout

```
src/triage_ai/
├── __init__.py
├── config.py          # pydantic-settings Settings model
├── main.py            # Typer CLI
├── data/loader.py     # JSON → SupportTicket loader
├── llm/client.py      # ChatOpenRouter model factory
└── models/ticket.py   # SupportTicket Pydantic model
```

## Tests

```bash
uv run pytest
```

## Documentation

- [`docs/HANDOFF.md`](docs/HANDOFF.md) — current project state and next steps.
- [`CHANGELOG.md`](CHANGELOG.md) — version history.

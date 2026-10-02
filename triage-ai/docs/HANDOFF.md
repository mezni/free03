# Project Handoff

Status of the **triage-ai** project at the end of this working session.

## Project Goal

An AI-powered support-ticket triage assistant. The CLI loads seed support tickets
from JSON and will eventually route each ticket through an LLM (OpenRouter) to
classify, prioritize, and draft a response.

## What Exists (working, tested)

### Architecture (`src/triage_ai/`)

| Package      | Purpose                                                            |
| ------------ | ------------------------------------------------------------------ |
| `config.py`  | `Settings` via pydantic-settings; reads `.env`. Current fields:    |
|              | `app_name`, `environment`, `debug`, `openrouter_api_key`,           |
|              | `openrouter_model`. `settings` singleton exposed.                   |
| `main.py`    | Typer CLI. Commands: `info`, `tickets`.                            |
| `models/`    | `SupportTicket` Pydantic model (`ticket_id`, `customer_id`,         |
|              | `subject`, `description`) with validation.                          |
| `data/`      | `loader.load_tickets()` — reads `data/tickets.json` into           |
|              | `SupportTicket` objects.                                            |
| `llm/`       | `client.create_chat_model()` — `ChatOpenRouter` factory wired to    |
|              | settings. **Not yet wired into the CLI.**                           |

### Data

- `data/tickets.json` — 10 seed tickets (T-1001 .. T-1010).
- `.env.example` — template: app settings + `OPENROUTER_API_KEY`,
  `OPENROUTER_MODEL`.
- Local `.env` exists (gitignored) for development.

### Tests — all passing (`uv run pytest` → 6 passed)

- `tests/test_config.py` — settings defaults.
- `tests/test_ticket.py` — model creation + validation errors.
- `tests/test_loader.py` — `load_tickets()` reads 10 tickets; objects are
  Pydantic models.

### CLI (verified working)

```
uv run triage-ai info      # app name, environment, debug
uv run triage-ai tickets   # lists T-1001..T-1010 with subjects
```

## Next Steps (not yet done)

1. **Wire the LLM into the CLI** — add a `/triage` (or `/classify`) command that
   calls `create_chat_model()` for a selected ticket. Recommend adding
   `ChatPromptTemplate` + `StrOutputParser` (langchain-core already present).
2. **Environment note** — `create_chat_model()` reads `OPENROUTER_API_KEY` from
   `.env`. A missing/blank key currently raises at import of `config.settings`.
   Decide desired behavior (fail fast vs. lazy init per command).
3. **Versioning** — next release is **0.1.5** (per CHANGELOG convention); keep
   `CHANGELOG.md` version table + sections updated with each release.

## Conventions

- Package layout: `src/`-style; import as `from triage_ai...`.
- Package manager: `uv` (`uv add`, `uv run`, `uv run pytest`).
- CLI entry point: `triage-ai` script → `triage_ai.main:app` (Typer + rich).
- Tests live in `tests/`; run with `uv run pytest`.
- Changelog: Keep-a-Changelog style; every release updates both the version
  history table and the per-version sections.

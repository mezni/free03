# ticket-triage — Baseline

## Summary

A small CLI program that classifies a customer-support ticket using the
Anthropic API. It loads sample tickets from `data/tickets.json`, takes the
first one, sends it to an LLM with a triage system prompt, and prints the
resulting **category**, **priority**, **reasoning**, and a **draft response**.

### Program flow

```mermaid
flowchart TD
    A[Start: uv run python -m support_agent.main] --> B[main.py: read data/tickets.json]
    B --> C[Load tickets JSON list]
    C --> D[Build SupportTicket from tickets[0] via pydantic model_validate]
    D --> E[agent.py: triage_ticket&#40;ticket&#41;]
    E --> F[ask_llm: send TRIAGE_SYSTEM_PROMPT + ticket.message to Anthropic]
    F --> G{API key configured?}
    G -- no --> ERR1["RuntimeError: ANTHROPIC_API_KEY not configured"] --> O[End]
    G -- yes --> H[Parse LLM JSON response via _extract_json]
    H --> I{Fenced or prose-wrapped JSON?}
    I -- ```json fence --> J[Strip fence]
    I -- prose/prefix --> K[Extract first {...} block]
    J --> L[json.loads]
    K --> L
    L --> M[Validate into TriageResult via model_validate]
    M --> N["Print Ticket + TriageResult (pretty JSON)"]
    N --> O
```

### Structure

```
ticket-triage/
├── docs/01_baseline.md
├── data/tickets.json            # sample support tickets
├── support_agent/
│   ├── __init__.py
│   ├── agent.py                 # models + prompt + LLM triage logic
│   └── main.py                  # CLI entrypoint (read ticket, call triage, print)
├── tests/test_triage.py         # pytest tests for the pydantic models
├── pyproject.toml               # uv project config & deps
├── uv.lock
└── .env                         # ANTHROPIC_API_KEY, ANTHROPIC_MODEL
```

### Key components

- **`SupportTicket`** — pydantic model for a ticket (`ticket_id`, `customer_id`, `message`).
- **`TicketCategory` / `TicketPriority`** — enums constraining the LLM output
  (category: account/billing/technical/product/shipping/other; priority:
  low/medium/high/urgent).
- **`TriageResult`** — validated LLM output (`category`, `priority`, `reasoning`, `response`).
- **`task_llm` / `ask_llm`** — sends `TRIAGE_SYSTEM_PROMPT` + ticket message to
  `client.messages.create` on the Anthropic API.
- **`_extract_json`** — robustly parses the LLM reply: handles raw JSON, markdown
  code fences, and prose-wrapped responses by extracting the first `{...}` block.
- **`triage_ticket`** — orchestrates ask + parse + validate.
- **`main`** — entrypoint: reads the first ticket from the JSON file, triages it,
  prints the message and the pretty-printed `TriageResult`.

### Running

```bash
uv run python -m support_agent.main   # run from ticket-triage/
uv run pytest                        # run the test suite
```

> Baseline doc — captured at commit-time state. Keep as reference while the
> program evolves.
# Session Handoff

Project: Support Ticket Triage Agent. Experiments and CHANGELOG track the plan.

## Current Status

- **Baseline experiments (01–04):** complete. Plain LLM baseline → ticket baseline → structured extraction (JSON failure modes) → deliberately bad tool schema.
- **Extraction + triage pipeline:** complete. `extract_ticket()` then `decide_triage()` across all sample tickets.
- **Agent loop:** complete. `tool_use`/`tool_result` loop bounded by `max_iterations`, executes **all** tool calls in a turn before returning text (fixes the earlier preamble bug).
- **Structure into agent:** complete. Agent receives original ticket (subject + body), structured extraction, and triage decision; triage is an explicit constraint in the system prompt.
- **Action tools:** complete. `create_ticket` and `escalate_to_human` with Pydantic-validated input, JSON-file stores, registry, and tests.
- **Registry cleanup:** complete. `TOOL_FUNCTIONS` + `TOOL_SCHEMAS`; agent no longer imports individual tools.

## What's Built

- `src/support_agent/client.py` — `chat()` / `chat_with_tools()` around the Anthropic Messages API (model `claude-haiku-4-5-20251001`).
- `src/support_agent/models/` — `ticket.py` (`SupportTicket`, `TicketExtraction`, `TriageResult`, `TriageDecision`), `tools.py` (`CreateTicketInput/Result`), `escalation.py` (`EscalateToHumanInput/Result`).
- `src/support_agent/prompts.py` — extraction and triage system prompts.
- `src/support_agent/extraction.py` — `extract_ticket()`: prompt → LLM → JSON → Pydantic.
- `src/support_agent/triage.py` — `decide_triage()`: extraction → LLM → `TriageDecision`.
- `src/support_agent/agent.py` — `run_agent()`: agent loop over all registered tools; returns joined text only when no tool calls remain; raises `RuntimeError` past `max_iterations` (default 5).
- `src/support_agent/run_agent.py` — full pipeline runner: load → extract → triage → agent, passing `Subject:` + `Message:`.
- `src/support_agent/main.py` — earlier extract + triage-only runner.
- `src/support_agent/tool_experiment.py` — single tool-call experiment runner.
- Tools: `tools/schemas.py` (`KNOWLEDGE_BASE_SEARCH_TOOL`, `CREATE_TICKET_TOOL`, `ESCALATE_TO_HUMAN_TOOL`), `tools/registry.py` (`TOOL_FUNCTIONS`, `TOOL_SCHEMAS`), `tools/dispatcher.py` (`dispatch_tool`), `tools/knowledge_base.py`, `tools/ticketing.py`, `tools/escalation.py`.
- Data: `data/knowledge_base.json` (KB001–KB005), `data/tickets/tickets.json` (T001–T006), `data/created_tickets.json` (`[]`), `data/escalations.json` (`[]`).
- Tests: `test_knowledge_base.py`, `test_tool_dispatcher.py`, `test_escalation.py` — **9 passed**, all offline (JSON stores isolated via `tmp_path`/`monkeypatch`).
- Docs: `docs/experiments/01_baseline.md` … `05_agent_with_triage.md`; `CHANGELOG.md` with released history 0.1.1–0.1.11; this handoff.

## Verified Live Runs

- Single tool call (`tool_experiment.py`) with the good schema: model requested a meaningful query (`internet down troubleshooting router restart`).
- Full pipeline (`run_agent.py`) ran across all 6 tickets — extraction, triage, then an agent turn. In the pre-fix loop the agent returned only the preamble text and dropped its tool call; after the clean loop rewrite this is resolved (all `tool_use` blocks execute before text is returned).

## Next Steps

1. **Experiment 06** — run the full agent with action tools against the sample tickets and record KB usage, query quality, ticket creation, and escalation behavior in `docs/experiments/06_action_tools.md`.
2. Observe whether the model correctly avoids creating duplicate tickets and only escalates when `needs_escalation` is true.
3. Consider whether the triage decision should reset `data/created_tickets.json` / `data/escalations.json` before live runs (stores are currently persistent).
4. Open design question (predecessor project): how to guard against model text contradicting tool records.

## Run

```bash
uv sync
uv run pytest -q          # 9 passed
uv run ruff check .
uv run python src/support_agent/run_agent.py      # full live pipeline
uv run python src/support_agent/tool_experiment.py # single tool-call demo
```

## Loose Ends

- `ruff format .` intentionally NOT applied (hand-formatted; `ruff format --check` will flag).
- `data/created_tickets.json` and `data/escalations.json` accumulate across live runs — no reset/cleanup logic yet.
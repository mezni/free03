# Session Handoff

Project: Support Ticket Triage Agent. Experiments and CHANGELOG track the plan.

## Current Status

- **Baseline experiments (01–04):** complete. Plain LLM baseline → ticket baseline → structured extraction (JSON failure modes) → deliberately bad tool schema.
- **Extraction + triage pipeline:** complete. `extract_ticket()` then `decide_triage()` across all sample tickets.
- **Agent loop:** complete. `tool_use`/`tool_result` loop bounded by `max_iterations`, executes **all** tool calls in a turn before returning text (fixes the earlier preamble bug).
- **Structure into agent:** complete. Agent receives original ticket (subject + body), structured extraction, and triage decision; triage is an explicit constraint in the system prompt.
- **Action tools:** complete. `create_ticket` and `escalate_to_human` with Pydantic-validated input, JSON-file stores, registry, and tests.
- **Registry cleanup:** complete. `TOOL_FUNCTIONS` + `TOOL_SCHEMAS`; agent no longer imports individual tools.
- **Guardrails:** complete. `GuardrailViolation` exception, `validate_extraction_output()`, `validate_triage_output()`/`validate_triage_decision()`, `validate_escalation()` — prevent invalid JSON, schema violations, security tickets without escalation, and escalation without high/critical priority.
- **Tool permission sets:** complete. `READ_ONLY_TOOLS` = {"knowledge_base_search", "search_similar_tickets"}, `STATE_CHANGING_TOOLS` = {"create_ticket", "escalate_to_human"} — used by dispatcher `allowed_tools` filter.
- **Historical ticket search:** complete. `search_similar_tickets()` keyword‑matching against `data/historical_tickets.json`; `SimilarTicket` model with relevance scoring.
- **Evaluation framework:** complete. `EvaluationCase`/`EvaluationResult`/ `EvaluationSummary` Pydantic models, `load_evaluation_cases()`, `evaluate_extraction()`, `evaluate_triage()`, `evaluate_case()`, and `scripts/run_evaluation.py` runner reporting per‑check PASS/FAIL and overall pass rate.
- **Multi‑agent handoff:** complete. `ResearchRequest`/`ResearchResult` Pydantic contracts; `RESEARCH_AGENT_TOOLS` (only `search_similar_tickets`); `SUPPORT_AGENT_TOOLS` (knowledge_base, create_ticket, escalate_to_human); orchestrator workflow from support agent to research agent and back.

## What's Built

- `src/support_agent/client.py` — `chat()` / `chat_with_tools()` around the Anthropic Messages API (model `claude-haiku-4-5-20251001`).
- `src/support_agent/models/` — `ticket.py` (`SupportTicket`, `TicketExtraction`, `TriageResult`, `TriageDecision`), `tools.py` (`CreateTicketInput/Result`), `escalation.py` (`EscalateToHumanInput/Result`), `evaluation.py` (`EvaluationCase`, `EvaluationResult`, `EvaluationSummary`), `research.py` (`HistoricalTicket`, `SimilarTicket`), `handoff.py` (`ResearchRequest`, `ResearchResult`, `SimilarTicket`).
- `src/support_agent/prompts.py` — extraction and triage system prompts.
- `src/support_agent/guardrails.py` — `GuardrailViolation`, `validate_extraction_output`, `validate_triage_output`/`validate_triage_decision`, `validate_escalation`.
- `src/support_agent/tools/` — `schemas.py` (`KNOWLEDGE_BASE_SEARCH_TOOL`, `CREATE_TICKET_TOOL`, `ESCALATE_TO_HUMAN_TOOL`, `SEARCH_SIMILAR_TICKETS_TOOL`), `registry.py` (`TOOL_FUNCTIONS`, `TOOL_SCHEMAS`), `dispatcher.py` (`dispatch_tool` with `allowed_tools` filter), `knowledge_base.py`, `ticketing.py`, `escalation.py`.
- `src/support_agent/memory/` — `conversation.py` (`ConversationMemory`), `__init__.py`.
- `src/support_agent/research_agent.py` — `run_research_agent(ResearchRequest)` using `search_similar_tickets` only.
- `src/support_agent/orchestrator.py` — `build_research_request()`, `research_ticket()`.
- `src/support_agent/agent.py` — `run_agent()` with `research` parameter and context injection; `SUPPORT_AGENT_TOOLS` only.
- `scripts/run_evaluation.py` — evaluation runner comparing extraction/triage against `EvaluationCase` expectations.
- Data: `data/knowledge_base.json` (KB001–KB005), `data/tickets/tickets.json` (T001–T006), `data/historical_tickets.json` (H001–H005), `data/created_tickets.json` (`[]`), `data/escalations.json` (`[]`), `data/evaluation_cases.json` (EVAL001–EVAL005).
- Tests: `test_knowledge_base.py`, `test_tool_dispatcher.py`, `test_escalation.py`, `test_handoff.py`, `test_historical_tickets.py`, `test_escalation.py` — **14 passed**, all offline (JSON stores isolated via `tmp_path`/`monkeypatch`).
- Docs: `docs/experiments/01_baseline.md` … `11_multi_agent_handoff.md`; `CHANGELOG.md` with released history 0.1.1–0.1.16; this handoff.

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
uv run pytest -q          # 14 passed
uv run ruff check .
uv run python src/support_agent/run_agent.py      # full live pipeline
uv run python src/support_agent/tool_experiment.py # single tool-call demo
uv run uv run python scripts/run_evaluation.py     # evaluation runner
```

## Loose Ends

- `ruff format .` intentionally NOT applied (hand-formatted; `ruff format --check` will flag).
- `data/created_tickets.json` and `data/escalations.json` accumulate across live runs — no reset/cleanup logic yet.
- Evaluation pass rates per check (product/priority/category/urgency/escalation) should be monitored for model improvement.
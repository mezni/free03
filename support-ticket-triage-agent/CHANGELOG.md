# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Version Summary

| Version | Feature Domain | Key Objectives |
| --- | --- | --- |
| 0.1.9 | Tool Registry & Agent Loop Cleanup | Centralize schemas + functions in a registry; fix the loop to run all tool calls before answering. |
| 0.1.8 | Agent with Triage Context | Feed extraction + triage into the agent; make triage an explicit constraint. |
| 0.1.7 | Agent Loop | Run the `tool_use`/`tool_result` loop over the KB search tool with a maximum-iteration guard. |
| 0.1.6 | Tool Schema Engineering | Replace a deliberately bad tool schema with a designed `knowledge_base_search` schema; add a tool dispatcher. |
| 0.1.5 | Knowledge-Base Tool | Ground answers by keyword-searching a fake knowledge base with a registered tool. |
| 0.1.4 | Triage Decision | Classify category/urgency plus knowledge-search and escalation flags from the extracted ticket. |
| 0.1.3 | Structured Extraction | Extract `customer_id`, `product`, `sentiment`, and `priority` from free-form tickets into Pydantic models. |
| 0.1.2 | First LLM Application | Wrap the Anthropic Messages API and parse model JSON output. |
| 0.1.1 | Foundation | Set up the `uv` project, package layout, sample data, and experiment docs. |

## [0.1.9] — Tool Registry & Agent Loop Cleanup

- Consolidated `src/support_agent/tools/registry.py` into `TOOL_FUNCTIONS` (name → implementation) and `TOOL_SCHEMAS` (list of tool schemas); the registry now owns both sides of the tool contract.
- Updated `src/support_agent/tools/dispatcher.py` to resolve tools from `TOOL_FUNCTIONS`.
- Refactored `src/support_agent/agent.py` to import only `TOOL_SCHEMAS` (no direct tool imports), collect all `tool_use` blocks per turn, execute every requested tool, and return the joined text only when no tool calls remain — fixing the bug where the agent dropped its KB search and answered with just the preamble.
- Added `test_unknown_tool_raises_error` to `tests/test_tool_dispatcher.py` asserting `ValueError` for unregistered tools; updated `tests/test_knowledge_base.py` to the renamed `TOOL_FUNCTIONS` (4 tests passing).

## [0.1.8] — Agent with Triage Context

- Extended `run_agent()` to accept `extraction: TicketExtraction` and `triage: TriageDecision`, embedding the ticket plus structured extraction and triage decision in the user message.
- Updated the system prompt with triage constraints: no KB search when `needs_knowledge_search` is false (unless required for safety), no returning the case as resolved when `needs_escalation` is true, no inventing policies/refunds/account changes.
- Replaced the standalone `run_agent.py` experiment with the full pipeline runner: `load_tickets` → `extract_ticket` → `decide_triage` → `run_agent` across all tickets.
- Added experiment documentation `docs/experiments/05_agent_with_triage.md`, recording that the agent drops the KB tool call when the loop returns on the first text block (open fix: defer text until tool calls in the turn are resolved).

## [0.1.7] — Agent Loop

- Added `src/support_agent/agent.py` `run_agent()` implementing the `tool_use`/`tool_result` loop over `KNOWLEDGE_BASE_SEARCH_TOOL`, dispatching calls through `dispatch_tool()` and feeding results back to the model.
- Bounded the loop with `max_iterations` (default 5), raising `RuntimeError` if the agent exceeds the cap.
- Added `src/support_agent/run_agent.py` CLI runner demonstrating a live internet-troubleshooting ticket.

## [0.1.6] — Tool Schema Engineering

- Removed the deliberately bad schema (`name: search`, generic `input` parameter, "Search stuff." description) from `src/support_agent/tools/schemas.py`.
- Added `KNOWLEDGE_BASE_SEARCH_TOOL` in `src/support_agent/tools/schemas.py` with a descriptive name, a purpose-explaining description, and a required `query` parameter with `additionalProperties: false`.
- Updated `src/support_agent/tool_experiment.py` to use `KNOWLEDGE_BASE_SEARCH_TOOL`; live run confirmed the model now requests a meaningful query (`internet down troubleshooting router restart`).
- Added `src/support_agent/tools/dispatcher.py` `dispatch_tool()` — resolves a tool name from `TOOLS` and raises `ValueError` for unknown tools.
- Added `tests/test_tool_dispatcher.py` verifying dispatch of the knowledge-base search.
- Added experiment documentation `docs/experiments/03_structured_extraction.md` and `docs/experiments/04_bad_tool_schema.md`.

## [0.1.5] — Knowledge-Base Tool

- Added `src/support_agent/tools/knowledge_base.py` `knowledge_base_search(query)` — keyword-scoring search returning the top three articles from `data/knowledge_base.json`.
- Added `src/support_agent/tools/registry.py` mapping `knowledge_base_search` to the implementation.
- Added offline tests in `tests/test_knowledge_base.py`.

## [0.1.4] — Triage Decision

- Added `decide_triage()` in `src/support_agent/triage.py` running extraction → LLM → `TriageDecision`.
- Added `src/support_agent/main.py` CLI runner chaining extraction and triage across all tickets.
- Added `src/support_agent/tool_experiment.py` experiment runner for single tool-call behavior.

## [0.1.3] — Structured Extraction

- Added `SupportTicket`, `TicketExtraction`, `TriageResult`, and `TriageDecision` models in `src/support_agent/models/ticket.py`, with enum-constrained `product`, `sentiment`, `priority`, `category`, and `urgency`.
- Added extraction and triage system prompts in `src/support_agent/prompts.py`.
- Added `src/support_agent/extraction.py` `extract_ticket()` running prompt → LLM → JSON → Pydantic validation.
- Added experiment documentation `docs/experiments/01_baseline.md` and `docs/experiments/02_ticket_baseline.md`.

## [0.1.2] — First LLM Application

- Added `src/support_agent/client.py` with `chat()` and `chat_with_tools()` wrappers around the Anthropic Messages API (model `claude-haiku-4-5-20251001`).
- Added `src/support_agent/json_utils.py` for robust JSON parsing of model output.

## [0.1.1] — Foundation

- Initialized `uv` project (`pyproject.toml`, `uv.lock`, virtualenv) with a `src` layout.
- Added runtime dependencies: `anthropic`, `pydantic`, `python-dotenv`.
- Added development dependency: `pytest`.
- Added `.env.example` and gitignored local `.env`.
- Scaffolded package layout under `src/support_agent/` and `tests/`.
- Added sample datasets `data/knowledge_base.json` and `data/tickets/tickets.json`.

## Commands

```bash
uv sync
uv run pytest        # 4 passed
uv ruff check .
uv run python src/support_agent/main.py                  # extract + triage pipeline
uv run python src/support_agent/tool_experiment.py       # live tool-call demo
uv run python src/support_agent/run_agent.py             # live agent-loop demo
```
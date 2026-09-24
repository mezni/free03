# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Version Summary

| Version | Feature Domain | Key Objectives |
| --- | --- | --- |
| 0.1.0 (unreleased) | Foundation | Set up the `uv` project, package layout, sample data, and experiment docs. |
| 0.1.0 (unreleased) | Structured Extraction | Extract `customer_id`, `product`, `sentiment`, and `priority` from free-form tickets into Pydantic models. |
| 0.1.0 (unreleased) | Triage Decision | Classify category/urgency plus knowledge-search and escalation flags from the extracted ticket. |
| 0.1.0 (unreleased) | Knowledge-Base Tool | Ground answers by keyword-searching a fake knowledge base with a registered tool. |
| 0.1.0 (unreleased) | Tool Schema Engineering | Replace a deliberately bad tool schema with a designed `knowledge_base_search` schema; add a tool dispatcher. |
| 0.1.0 (unreleased) | Agent Loop | Run the `tool_use`/`tool_result` loop over the KB search tool with a maximum-iteration guard. |

## [Unreleased]

### Foundation

- Initialized `uv` project (`pyproject.toml`, `uv.lock`, virtualenv) with a `src` layout.
- Added runtime dependencies: `anthropic`, `pydantic`, `python-dotenv`.
- Added development dependency: `pytest`.
- Added `.env.example` and gitignored local `.env`.
- Scaffolded package layout under `src/support_agent/` and `tests/`.
- Added sample datasets `data/knowledge_base.json` and `data/tickets/tickets.json`.

### First LLM Application

- Added `src/support_agent/client.py` with `chat()` and `chat_with_tools()` wrappers around the Anthropic Messages API (model `claude-haiku-4-5-20251001`).
- Added `src/support_agent/json_utils.py` for robust JSON parsing of model output.

### Structured Extraction

- Added `SupportTicket`, `TicketExtraction`, `TriageResult`, and `TriageDecision` models in `src/support_agent/models/ticket.py`, with enum-constrained `product`, `sentiment`, `priority`, `category`, and `urgency`.
- Added extraction and triage system prompts in `src/support_agent/prompts.py`.
- Added `src/support_agent/extraction.py` `extract_ticket()` running prompt → LLM → JSON → Pydantic validation.
- Added `src/support_agent/triage.py` `decide_triage()` running extraction → LLM → `TriageDecision`.
- Added `src/support_agent/main.py` CLI runner chaining extraction and triage across all tickets.
- Added `src/support_agent/tool_experiment.py` experiment runner for single tool-call behavior.
- Added experiment documentation `docs/experiments/01_baseline.md` and `docs/experiments/02_ticket_baseline.md`.

### Knowledge-Base Tool

- Added `src/support_agent/tools/knowledge_base.py` `knowledge_base_search(query)` — keyword-scoring search returning the top three articles from `data/knowledge_base.json`.
- Added `src/support_agent/tools/registry.py` mapping `knowledge_base_search` to the implementation.
- Added offline tests in `tests/test_knowledge_base.py`.

### Tool Schema Engineering

- Removed the deliberately bad schema (`name: search`, generic `input` parameter, "Search stuff." description) from `src/support_agent/tools/schemas.py`.
- Added `KNOWLEDGE_BASE_SEARCH_TOOL` in `src/support_agent/tools/schemas.py` with a descriptive name, a purpose-explaining description, and a required `query` parameter with `additionalProperties: false`.
- Updated `src/support_agent/tool_experiment.py` to use `KNOWLEDGE_BASE_SEARCH_TOOL`; live run confirmed the model now requests a meaningful query (`internet down troubleshooting router restart`).
- Added `src/support_agent/tools/dispatcher.py` `dispatch_tool()` — resolves a tool name from `TOOLS` and raises `ValueError` for unknown tools.
- Added `tests/test_tool_dispatcher.py` verifying dispatch of the knowledge-base search.
- Added experiment documentation `docs/experiments/03_structured_extraction.md` and `docs/experiments/04_bad_tool_schema.md`.

### Agent Loop

- Added `src/support_agent/agent.py` `run_agent()` implementing the `tool_use`/`tool_result` loop over `KNOWLEDGE_BASE_SEARCH_TOOL`, dispatching calls through `dispatch_tool()` and feeding results back to the model.
- Bounded the loop with `max_iterations` (default 5), raising `RuntimeError` if the agent exceeds the cap.
- Added `src/support_agent/run_agent.py` CLI runner demonstrating a live internet-troubleshooting ticket.

## Commands

```bash
uv sync
uv run pytest        # 3 passed
uv ruff check .
uv run python src/support_agent/main.py                  # extract + triage pipeline
uv run python src/support_agent/tool_experiment.py       # live tool-call demo
uv run python src/support_agent/run_agent.py             # live agent-loop demo
```
# Changelog

All notable changes to **relay-agent** are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned

- Human-in-the-loop approval gates before final synthesis
- Local PDF / CSV document ingestion for multi-modal research
- LangSmith observability integration

---

## [0.1.0] - 2026-10-17

First public release: a modular, production-grade multi-agent research and
synthesis engine built on LangGraph.

### Added

#### Core engine

- Supervisor–worker state graph with conditional routing and `FINISH` termination
  (`31418ef` — `src/workflows/graph.py`, `src/workflows/state.py`)
- Supervisor router using Pydantic structured output to choose
  `Researcher` / `Writer` / `FINISH` (`src/agents/supervisor.py`)
- Researcher agent with DuckDuckGo `web_search` tool binding and manual
  `ToolMessage` execution loop (`c631693` — `src/agents/researcher.py`,
  `src/tools/search.py`)
- Writer agent that synthesizes research notes into markdown reports
  (`src/agents/writer.py`)
- `operator.add` message reducer on `AgentState` for safe, append-only
  conversation history

#### Persistence

- LangGraph SQLite checkpointer (`SqliteSaver`) writing to
  `checkpoints.sqlite`, with `thread_id`-scoped sessions across CLI and UI
  (`35f559b`)

#### Interfaces

- CLI runner with streaming node transitions, route decisions, and tool-call
  logging (`0a77193` — `src/main.py`)
- Streamlit workspace UI with chat history, node-status expanders, and a
  sidebar session/thread manager (`4bef770` — `app.py`)

#### Evaluation

- Golden query dataset (`evals/datasets/golden_queries.json`)
- Deterministic tool-selection metric (`evals/metrics/tool_usage.py`)
- LLM-as-a-judge correctness metric grading key-fact coverage from `0.0` to
  `1.0` with GPT-4o (`evals/metrics/correctness.py`)
- Pytest harness parametrized over the benchmark set, asserting
  `tool_score == 1.0` and `correctness_score >= 0.8`
  (`0f84766`)

#### Delivery & tooling

- Project scaffolding and dependency locking with `uv`
  (`4a58874` — `pyproject.toml`, `uv.lock`)
- Multi-stage `Dockerfile` and `docker-compose.yml` for web app deployment
  (`9307483`)
- GitHub Actions CI running `ruff` linting and the pytest evaluation suite on
  every push and pull request (`be6a3d2` — `.github/workflows/ci.yml`)
- Ruff lint/import-sort configuration and pytest `testpaths` covering both
  `tests/` and `evals/`

### Changed

- Repository history consolidated during cleanup; experimental modules from
  earlier iterations were removed from the tree (`14ebeb5`, `6ec9999`)

---

## Earlier internal iterations (2026-10-10 → 2026-10-14)

Pre-release experiments that informed the current architecture. These were
superseded and cleaned up before `0.1.0`; they are listed for historical
context only.

- **Data layer** — SQLite persistence with revision-based concurrency control,
  routing, persistence, and an application service layer with typed
  architectural boundaries (`fbd7b79`, `fb36eec`)
- **HTTP API** — request validation, API authentication with role-based
  authorization, centralized validated configuration (`5cdfc6c`, `4b0e4f2`,
  `52ccda9`)
- **Reliability** — retry policies, timeouts, rate limiting and concurrency
  control, resilience and error handling (`7fbc585`, `80d5867`, `8c849ac`,
  `376aba4`)
- **Async & background processing** — background jobs, job queue integration,
  outbox pattern, event-driven and distributed workflows, durable routing
  (`802e9c1` … `6f68fc5`)
- **Operations** — structured logging with correlation IDs, metrics and health
  checks, observability, SLIs/SLOs (`e76e850`, `79e16b4`, `4698f9f`,
  `0b7eacd`)
- **Quality & security** — automated quality gates, security hardening,
  security regression tests and threat model, Locust load-test scenario and
  capacity plan (`3a68d33`, `15a3d83`, `cd03f18`, `3796981`)

[Unreleased]: https://github.com/your-username/relay-agent/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/your-username/relay-agent/releases/tag/v0.1.0

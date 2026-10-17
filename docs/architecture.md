# 🏗 Architecture & Technical Specification — `relay-agent`

`relay-agent` is a production-grade, modular multi-agent research and synthesis
engine built with **LangGraph**, **LangChain**, and **OpenAI**. It features a
dynamic supervisor–worker architecture, persistent state checkpointer memory,
automated LLM-as-a-judge benchmarking, and dual execution interfaces (CLI and
Streamlit UI).

## Overview

| Concern                  | Choice                                                         |
| :----------------------- | :------------------------------------------------------------- |
| Orchestration            | LangGraph `StateGraph` with conditional edges                  |
| Language model           | OpenAI `gpt-4o` (structured output for routing)                |
| Search tool              | DuckDuckGo (`web_search`)                                      |
| Persistence              | LangGraph `SqliteSaver` → `checkpoints.sqlite`                 |
| Evaluation               | Pytest + deterministic tool metric + LLM-as-a-judge            |
| Interfaces               | CLI streamer (`src/main.py`) + Streamlit UI (`app.py`)         |
| Tooling                  | `uv` · `ruff` · `pytest` · GitHub Actions · Docker             |

## Contents

1. [System Topology & Dynamic Routing](#1-system-topology--dynamic-routing)
2. [State Schema & Reducer Mechanics](#2-state-schema--reducer-mechanics)
3. [Persistent Checkpointing & State Memory](#3-persistent-checkpointing--state-memory)
4. [Evaluation Suite & Quality Assurance](#4-evaluation-suite--quality-assurance-evals)
5. [Execution Interfaces](#5-execution-interfaces)
6. [Containerization & CI/CD Pipeline](#6-containerization--cicd-pipeline)

---

## 1. System Topology & Dynamic Routing

The system follows a **Supervisor–Worker (Router)** pattern. Rather than
enforcing a rigid linear pipeline, execution flow is governed dynamically by a
state graph where a central supervisor node inspects conversation history and
makes deterministic routing decisions.

```text
                +------------------+
                |   User Prompt    |
                +--------+---------+
                         |
                         v
                +------------------+
                |    Supervisor    |<---+
                |  (Router Agent)  |    |  Loop / State
                +--+------------+--+    |  Feedback
                   |            |       |
     +-------------+            +----+  |
     |                               |  |
     v                               v  |
+-------------------+     +--------------------+
|  Researcher Agent |     |    Writer Agent    |
| (Fact Gathering)  |     | (Synthesis/Format) |
+---------+---------+     +----------+---------+
          |                          |
          +------------+-------------+
                       |
                       v
                  +---------+
                  |  END    |
                  +---------+
```

### Node Responsibilities

| Node                | Source                                    | Responsibility                                                                                                                                                           |
| :------------------ | :---------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Supervisor**      | `src/agents/supervisor.py`                | Central router. Uses Pydantic structured output (`with_structured_output`) to evaluate active state and decide the next target: `Researcher`, `Writer`, or `FINISH`.     |
| **Researcher**      | `src/agents/researcher.py`                | Fact-gathering agent equipped with the DuckDuckGo search wrapper (`src/tools/search.py`). Fetches live data and returns raw notes with tool-execution metadata.          |
| **Writer**          | `src/agents/writer.py`                    | Synthesis agent that converts raw research findings into clean, professional markdown reports.                                                                           |

### Routing Contract

```python
class RouterResponse(BaseModel):
    next_agent: Literal["Researcher", "Writer", "FINISH"]
```

- Workers always report back to the **Supervisor** (`Researcher → Supervisor`,
  `Writer → Supervisor`) so the router re-evaluates after every step.
- `FINISH` maps to LangGraph's `END` sentinel, terminating the loop.

---

## 2. State Schema & Reducer Mechanics

State is managed immutably using LangGraph's `TypedDict` pattern in
`src/workflows/state.py`:

```python
class AgentState(TypedDict):
    # Appends new messages automatically to the ongoing conversation list
    # using operator.add
    messages: Annotated[Sequence[BaseMessage], operator.add]
    # Stores the routing decision returned by the supervisor node
    next_agent: str
```

- **`operator.add` reducer** — ensures that when agents return new messages or
  tool outputs, they are safely *appended* to the historical state array rather
  than overwriting existing context.
- **`next_agent`** — the supervisor's routing decision; consumed by the
  conditional edge dispatcher and overwritten on each pass.

---

## 3. Persistent Checkpointing & State Memory

To support long-running research sessions and prevent context loss across
application reboots, `relay-agent` integrates **LangGraph SQLite Persistence**
(`SqliteSaver`).

| Aspect            | Detail                                                                |
| :---------------- | :-------------------------------------------------------------------- |
| Database file     | `checkpoints.sqlite`                                                  |
| Connection        | Single `sqlite3` connection opened with `check_same_thread=False`     |
| Isolation         | Every invocation is scoped by a `thread_id`                           |

Every `graph.stream(...)` / `graph.invoke(...)` call requires a thread
configuration dictionary:

```python
config = {"configurable": {"thread_id": "unique-session-id"}}
```

### Benefits

- Multi-turn chat memory in the Streamlit workspace UI
- Session continuity across executions and process restarts
- Independent, concurrent research threads (each test case and each UI session
  gets its own `thread_id`)

---

## 4. Evaluation Suite & Quality Assurance (`evals/`)

Multi-agent systems require rigorous verification. The `evals/` directory
provides continuous benchmarking executed via `pytest`.

| Component                              | Path                                         | Purpose                                                                                                          |
| :------------------------------------- | :------------------------------------------- | :--------------------------------------------------------------------------------------------------------------- |
| **Golden Dataset**                     | `evals/datasets/golden_queries.json`         | Curated test queries mapped to expected tool calls and ground-truth key facts.                                   |
| **Tool Selection Metric**              | `evals/metrics/tool_usage.py`                | Deterministic code check verifying whether required tools (e.g. `web_search`) were invoked during the run.       |
| **LLM-as-a-Judge Correctness**         | `evals/metrics/correctness.py`               | Grades final-output factual accuracy and key-fact coverage on a `0.0`–`1.0` scale using GPT-4o.                  |
| **Pytest Harness**                     | `evals/test_evals.py`                        | Parametrizes over benchmark datasets during local runs and GitHub Actions CI pipelines.                          |

### Quality gates enforced per test case

- `tool_score == 1.0` — every expected tool must have been called
- `correctness_score >= 0.8` — LLM judge score must meet the threshold

---

## 5. Execution Interfaces

The system provides two native interfaces sharing the same underlying state
graph:

### CLI Execution Runner — `src/main.py`

Streams real-time graph node transitions, route decisions, tool request
arguments, and agent output chunks to standard output:

```bash
uv run python src/main.py
```

### Streamlit Workspace UI — `app.py`

Interactive web interface featuring:

- Chat history with persisted thread memory
- Real-time status expanders showing node execution steps
- Sidebar session/thread manager for multiple concurrent research projects

```bash
uv run streamlit run app.py
```

---

## 6. Containerization & CI/CD Pipeline

| Concern                    | Tooling                                                                                                                      |
| :------------------------- | :--------------------------------------------------------------------------------------------------------------------------- |
| Dependency management      | [`uv`](https://github.com/astral-sh/uv) — fast lockfile resolution and virtualenv creation (`pyproject.toml`, `uv.lock`)     |
| Code quality               | `ruff` for linting and import sorting (`ruff check .`, `ruff format .`)                                                      |
| Containerization           | Multi-stage `Dockerfile` + `docker-compose.yml` for local web app deployment and CLI profiling                               |
| Continuous integration     | `.github/workflows/ci.yml` — GitHub Actions runs linting and the pytest evaluation suite on every push and pull request      |

---

*See also: [Product Overview & Requirements](product.md) · [README](../README.md)*

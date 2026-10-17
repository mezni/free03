<div align="center">

# ⚡ relay-agent

**A modular, high-performance Multi-Agent Research & Synthesis Engine built with LangGraph, `uv`, and `pytest`.**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Package Manager: uv](https://img.shields.io/badge/package--manager-uv-8A2BE2.svg)](https://github.com/astral-sh/uv)
[![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Framework: LangGraph](https://img.shields.io/badge/framework-LangGraph-orange.svg)](https://github.com/langchain-ai/langgraph)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

</div>

---

## 📌 Overview

**`relay-agent`** is a production-ready, event-driven multi-agent framework designed for complex, autonomous research and technical synthesis. Built on top of **LangGraph**, it replaces rigid sequential chains with a **Dynamic Supervisor Routing Architecture**. 

The system continuously evaluates incoming tasks, delegates research to specialized domain worker agents, routes outputs back to quality assurance/writers, and manages execution loops deterministically using state graphs.

---

## 🏛 System Architecture

The core architecture follows a **Supervisor-Worker Topology**. The Supervisor acts as a central orchestrator, reading state transitions and deciding the next execution node or signaling process completion (`FINISH`).

```text
                        ┌──────────────────┐
                        │   User Prompt    │
                        └────────┬─────────┘
                                 │
                                 ▼
                        ┌──────────────────┐
                        │    Supervisor    │◄───┐
                        │  (Router Agent)  │    │
                        └───┬──────────┬───┘    │
                            │          │        │
            ┌───────────────┘          └────────┼───────┐
            │                                   │       │ Loop
            ▼                                   ▼       │ State
  ┌──────────────────┐                ┌─────────────────┴┐
  │ Researcher Agent │                │   Writer Agent   │
  │ (Fact Gathering) │                │(Synthesis/Format)│
  └────────┬─────────┘                └─────────┬────────┘
           │                                    │
           └────────────────────────────────────┘
```

### Agent Roles

* 🎯 **Supervisor Node**: Evaluates global task progress using structured output and controls conditional state graph transitions.
* 🔍 **Researcher Node**: Executes tool calls (web search, data queries), extracts raw facts, and stores evidence in state.
* ✍️ **Writer Node**: Consolidates research findings into structured, publication-ready markdown reports.

---

## 📂 Project Structure

```text
relay-agent/
├── .env.example              # Environment variable template
├── README.md                 # Project documentation
├── pyproject.toml            # Project setup, dependencies, ruff, & pytest config
├── uv.lock                     # Deterministic dependency lockfile
│
├── config/                   # System configuration
│   ├── agents_config.yaml    # Agent personas, backstories, and models
│   └── settings.py           # Global settings & environment loaders
│
├── src/                      # Source code
│   ├── main.py               # Main CLI execution entrypoint
│   ├── agents/               # Supervisor, Researcher, and Writer nodes
│   │   ├── base_agent.py
│   │   ├── researcher.py
│   │   ├── supervisor.py
│   │   └── writer.py
│   ├── workflows/            # Graph state definitions and orchestration
│   │   ├── graph.py
│   │   └── state.py
│   ├── tools/                # Agent tools (web search, custom APIs)
│   │   └── search.py
│   └── utils/                # Logging, LLM factory, and helpers
│       ├── logger.py
│       └── llm_factory.py
│
├── evals/                    # 🧪 AI Behavioral Evaluation Suite
│   ├── conftest.py           # Pytest fixtures for agent evaluation
│   ├── datasets/             # Golden benchmarks and golden test queries
│   │   └── golden_queries.json
│   ├── metrics/              # Custom scorers (LLM-as-a-judge, tool accuracy)
│   │   ├── correctness.py
│   │   └── tool_usage.py
│   └── test_evals.py         # Pytest wrapper for benchmark execution
│
└── tests/                    # Unit and integration tests
    ├── test_agents.py
    └── test_workflows.py
```

---

## 🚀 Quickstart & Installation

This project uses [**`uv`**](https://github.com/astral-sh/uv) for fast, reliable Python package and environment management.

### 1. Prerequisites

Ensure you have `uv` installed on your machine:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Clone & Setup Workspace

```bash
# Clone repository
git clone https://github.com/your-username/relay-agent.git
cd relay-agent

# Sync virtual environment and install locked dependencies
uv sync
```

### 3. Environment Variables

Copy the example `.env` file and set your API keys:

```bash
cp .env.example .env
```

Edit `.env`:
```env
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here  # Optional for search tools
```

---

## 💻 Usage Examples

### 1. Execute via CLI Runner

Run an autonomous research query directly using `uv run`:

```bash
uv run python src/main.py
```

### 2. Programmatic Usage

You can import and run the compiled workflow graph inside your own Python application:

```python
from langchain_core.messages import HumanMessage
from src.workflows.graph import graph

def run_agent():
    prompt = "Analyze the structural differences between monolithic and microservices architecture."
    
    initial_state = {
        "messages": [HumanMessage(content=prompt)],
        "next_agent": "Supervisor"
    }

    # Stream execution nodes
    for event in graph.stream(initial_state):
        for node_name, output in event.items():
            print(f"⚡ [Executed Node]: {node_name}")
            if "messages" in output:
                print(f"📝 Output: {output['messages'][-1].content}\n")

if __name__ == "__main__":
    run_agent()
```

---

## 🧪 Testing, Evals & Code Quality

### Code Linting & Formatting (`ruff`)

`relay-agent` enforces high code quality standard using **Ruff**.

```bash
# Check code style and linting errors
uv run ruff check .

# Automatically fix linting and format files
uv run ruff check --fix .
uv run ruff format .
```

### Unit Tests & Multi-Agent Evals (`pytest`)

The project includes unit tests alongside an **LLM-as-a-Judge Evaluation Suite** (`evals/`) that tests factual accuracy, trajectory flow, and tool selection precision.

```bash
# Run unit tests and evaluation suite
uv run pytest

# Run with verbose logs to inspect evaluation scores
uv run pytest -v -s
```

---

## 🛡 License

This project is open-source and licensed under the [MIT License](LICENSE).

# 📦 Product Overview & Requirements — `relay-agent`

`relay-agent` is an autonomous multi-agent research and technical synthesis
platform designed to turn complex research queries into structured, verified
reports in seconds.

## Contents

1. [Vision & Core Value Proposition](#1-vision--core-value-proposition)
2. [Target User Personas](#2-target-user-personas)
3. [Key Feature Breakdown](#3-key-feature-breakdown)
4. [Product Roadmap](#4-product-roadmap)
5. [Success Metrics](#5-success-metrics)

---

## 1. Vision & Core Value Proposition

In technical research, developers and analysts spend considerable time
searching the web, filtering hallucinated or outdated documentation, and
synthesizing notes into readable summaries.

**`relay-agent`** solves this by assigning specialized AI agents to specific
stages of the research pipeline:

| Pillar                             | Why it matters                                                                           |
| :--------------------------------- | :--------------------------------------------------------------------------------------- |
| 🎯 **Autonomous Delegation**       | A central supervisor routes tasks dynamically based on intent.                           |
| 📚 **Fact-Grounded Output**        | Dedicated research nodes gather live external facts using web tools before writing.      |
| 🧵 **Persistent Memory**           | Multi-turn sessions persist across restarts via lightweight SQLite checkpointing.        |
| 📏 **Measured Accuracy**           | Built-in LLM-as-a-judge benchmarking keeps answers truthful and tool calls precise.      |

---

## 2. Target User Personas

| Persona                                    | Primary Needs                                                               | Key `relay-agent` Feature                                                 |
| :----------------------------------------- | :-------------------------------------------------------------------------- | :------------------------------------------------------------------------ |
| **Software Engineers & Architects**        | Rapid technology comparisons, release updates, architectural summaries      | Structured markdown outputs backed by factual web data                    |
| **AI Engineers & Researchers**             | Reference pattern for LangGraph multi-agent routing, persistence, evals     | Clean, modular Python codebase using `uv`, `pytest`, and `ruff`           |
| **Technical Product Managers**             | Automated market and technical briefing generation                          | Streamlit interactive UI with thread session management                   |

---

## 3. Key Feature Breakdown

### 🎯 Dynamic Supervisor Routing

- Evaluates incoming prompts and conversation state.
- Routes seamlessly between `Researcher` (fact retrieval) and `Writer`
  (output formatting).
- Handles iteration loops until the user's goal is met, then signals
  `FINISH`.

### 🧵 Persistent Workspace Memory

- SQLite checkpointer (`checkpoints.sqlite`) keeps full state history across
  runs.
- Thread isolation allows users to manage multiple concurrent research
  projects simultaneously in the Streamlit UI.

### 🧪 Quality & Evaluation Suite

- Benchmark dataset covering architecture synthesis and real-time research
  scenarios.
- Automated tool-usage assertions paired with GPT-4o LLM-as-a-judge grading.
- Integrated into `pytest` for continuous validation during code changes.

### 🐳 Developer Experience & Delivery

- Zero-config virtual environments and package locking via Astral `uv`.
- Full containerization with `Dockerfile` and `docker-compose.yml`.
- Automated GitHub Actions CI workflow for code linting (`ruff`) and test
  execution.

---

## 4. Product Roadmap

### ✅ Phase 1 — Core Engine & Evals *(Completed)*

- [x] LangGraph state machine with Supervisor–Worker architecture.
- [x] Web search tool binding for the Researcher agent.
- [x] Pytest evaluation framework with LLM-as-a-judge metric.
- [x] CLI streaming interface and Streamlit web UI.

### ✅ Phase 2 — Persistence & Containerization *(Completed)*

- [x] SQLite state checkpointing for long-term thread memory.
- [x] Multi-stage Docker build and Docker Compose configuration.
- [x] Automated GitHub Actions CI/CD pipeline.

### 🔮 Phase 3 — Future Enhancements *(Planned)*

- [ ] **Human-in-the-Loop (HITL)**: approval gates in Streamlit before final
      document synthesis.
- [ ] **Document Ingestion**: support uploading local PDFs and CSVs for
      multi-modal research.
- [ ] **Observability**: direct integration with LangSmith telemetry tracing.

---

## 5. Success Metrics

| Metric                          | Target                                             | Measured by                                                   |
| :------------------------------ | :------------------------------------------------- | :------------------------------------------------------------ |
| **Fact Accuracy Rate**          | ≥ 85% correctness score                            | LLM judge (`evals/metrics/correctness.py`)                    |
| **Tool Call Precision**         | 100% accuracy on queries requiring live search     | Deterministic tool metric (`evals/metrics/tool_usage.py`)     |
| **Build & Test Speed**          | < 30s total CI execution time                      | GitHub Actions with `uv` caching                              |

---

*See also: [Architecture & Technical Specification](architecture.md) · [README](../README.md)*

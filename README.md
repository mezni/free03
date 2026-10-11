# ticket-triage

A human-supervised AI ticket triage system. It analyzes incoming support tickets and recommends a category, priority, destination team, and a concise rationale. A human must review and approve a recommendation before any routing action is executed.

## Status

Early development. The documentation set (discovery, requirements, system design) is drafted and being validated. The core Python package is partially implemented, and the full test suite is not yet green.

See [`OVERVIEW.md`](OVERVIEW.md) for a project summary.

## Repository layout

```text
ticket-triage/
├── README.md
├── OVERVIEW.md
├── pyproject.toml
├── docs/
│   ├── 01-discovery/       # Business problem, stakeholders, metrics, constraints
│   ├── 02-requirements/    # Functional, non-functional, and acceptance criteria
│   ├── 03-system-design/   # Context, containers, data model, API, deployment, failures
│   └── progress/           # Daily learning and implementation notes (day-01 … day-07)
├── src/
│   └── ticket_triage/      # Python package (src layout)
└── tests/                  # pytest suite
```

## Documentation

| Phase | Location | Contents |
|---|---|---|
| 01 — Discovery | `docs/01-discovery/` | Discovery brief, stakeholder interviews, success metrics, assumptions and constraints |
| 02 — Requirements | `docs/02-requirements/` | Functional requirements (FR), non-functional requirements (NFR), acceptance criteria (AC) |
| 03 — System Design | `docs/03-system-design/` | System context, container diagram, sequence diagram, data model, API contracts, deployment, failure handling, ADRs |
| Progress notes | `docs/progress/` | Day-by-day notes and checklists |

## Package modules (`src/ticket_triage/`)

| Module | Responsibility |
|---|---|
| `domain.py` | Core data models: `Ticket`, `Recommendation`, `ApprovalDecision`, `RoutingOperation`, `TriageCase`, and the `Priority`, `CaseStatus`, `DecisionType`, `RoutingStatus` enums |
| `workflow.py` | Centralized case state-transition table and `InvalidTransitionError` |
| `classification.py` | `Classifier` protocol and a deterministic `FakeClassifier` |
| `policy.py` | `RecommendationPolicy` for validating recommendations against the approved taxonomy |
| `repositories.py` | `CaseRepository` protocol (persistence contract) |
| `application.py` | `TriageApplicationService` orchestrating use cases |

## Getting started

The project uses a `src/` layout and is installed as an editable package.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e .
.venv/bin/python -m pip install pytest
.venv/bin/python -m pytest -q
```

> Note: on this system `python` resolves to nothing; use `python3`. Packages are installed into a local virtual environment because the system Python is externally managed (PEP 668).

## Known gaps

- `validate_ticket` (`domain.py`) and `transition_case` (`workflow.py`) are referenced but not yet implemented, so `test_domain.py` and `test_workflow.py` fail at collection.
- Persistence adapter (`sqlite_repository.py`), approval (`approval.py`), and routing (`routing.py`) modules and their tests are not yet added.
- `application.py` and the end-to-end application test are incomplete.

The full suite currently stops at collection for the reasons above. Individual modules that are complete (classification and policy) pass under pytest.

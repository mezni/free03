# Project Overview — Ticket Triage AI

## What it is

`ticket-triage` is a human-supervised AI ticket triage system. It analyzes incoming customer support tickets and recommends a category, priority, destination team, and a concise rationale. A human must review and approve the recommendation before the system executes a routing action.

The architecture is intentionally technology-neutral until stakeholder discovery and requirements establish the constraints that justify specific choices.

## Business objective

Reduce the time support agents spend manually triaging tickets while maintaining or improving classification and routing quality.

Secondary objectives:

- Improve consistency of ticket classification.
- Reduce unnecessary reassignment.
- Provide explainable, auditable recommendations.
- Establish a measurable foundation for future automation.

## Problem

Support teams must read, categorize, prioritize, and route every incoming ticket. Manual triage can cause delay, inconsistent decisions, misrouting, and limited visibility into triage quality. These are treated as hypotheses to be confirmed through stakeholder interviews and operational data.

## Operating model

For each ticket the system aims to:

1. Ingest and normalize the ticket.
2. Request a structured recommendation from an LLM.
3. Validate the output against a schema and the approved taxonomy.
4. Apply deterministic routing, priority, and escalation rules.
5. Present the recommendation to an authorized human.
6. Execute the approved routing action only after approval.
7. Record the recommendation, decision, and outcome.

The LLM produces recommendations; application logic enforces validation, policy, authorization, workflow state, and execution control. Mandatory decisions require human approval.

## Scope

### In scope (initial MVP)

Ticket ingestion and normalization, classification recommendations, structured-output validation, deterministic policy, human approval workflow, approval-gated routing, workflow state persistence, ticketing integration, audit logging, and failure/fallback handling.

### Out of scope (initial MVP)

Autonomous routing without approval, automatic customer replies, automatic resolution or closure, multi-agent orchestration, and retrieval-augmented generation or a vector database without a demonstrated need.

## Requirements summary

The requirements phase (`docs/02-requirements/`) defines:

- **Functional requirements (FR-001 … FR-012):** ticket ingestion, normalization, category/priority/destination recommendations, recommendation validation, human review, approval-gated routing, audit trail, failure handling, operational monitoring, and configuration management.
- **Non-functional requirements (NFR-001 … NFR-011):** performance, classification quality, human oversight, reliability and recovery, security, privacy, auditability, scalability, maintainability, observability, and cost efficiency.
- **Acceptance criteria (AC-001 … AC-012):** testable scenarios covering valid and invalid input, classification, approval and rejection, unauthorized actions, timeouts, integration failures, duplicates, and auditability.

All numerical targets are provisional until approved by stakeholders.

## Proposed architecture

Documented in `docs/03-system-design/`.

**Logical components:** ticketing platform (external), ingestion/normalization, classification service, policy engine, approval workflow, workflow store, routing adapter, and audit/monitoring. These are logical responsibilities; the initial deployment is a single modular application plus one persistent data store.

**Key architecture decisions (ADRs):**

- **ADR-001:** Require human approval before routing.
- **ADR-002:** Separate LLM classification from deterministic business policy.
- **ADR-003:** Begin with a modular application rather than microservices.
- **ADR-004:** Define safe retry, idempotency, and reconciliation for routing actions.

**Cross-cutting design:** structured and validated model output, least-privilege access, data minimization, append-oriented audit records, explicit failure/reconciliation behavior, and observability that avoids exposing sensitive ticket content.

## Data model and workflow

The logical data model (`docs/03-system-design/data-model.md`) defines `TicketReference`, `TriageCase`, `Recommendation`, `ApprovalDecision`, `RoutingOperation`, and `AuditEvent`.

Case lifecycle:

```text
RECEIVED → PROCESSING → PENDING_APPROVAL → APPROVED → ROUTING → COMPLETED
                                     └────► REJECTED
Errors and unresolved conditions transition to MANUAL_REVIEW; retries may use RETRY_PENDING according to policy.
```

The routing operation has its own lifecycle (`pending`, `in_progress`, `succeeded`, `failed`, `outcome_unknown`, `reconciliation_required`) so that an unknown external outcome is never mislabeled as a definite failure.

## Success metrics

Defined in `docs/01-discovery/success-metrics.md`. Provisional pilot targets include at least a 30% reduction in median triage time, at least 95% routing accuracy, at least 95% priority agreement, at least 85% unmodified human acceptance, and 100% approval coverage and traceability. Baselines are not yet measured.

## Implementation status

**Documentation:** phases 01–03 drafted; daily progress notes in `docs/progress/day-01.md` … `day-07.md`.

**Python package (`src/ticket_triage/`):**

| Module | Status |
|---|---|
| `domain.py` | Implemented (enums and dataclasses for ticket, recommendation, decision, routing, case) |
| `workflow.py` | Partial — transition table and `InvalidTransitionError` present; `transition_case` not yet implemented |
| `classification.py` | Implemented — `Classifier` protocol and `FakeClassifier` |
| `policy.py` | Implemented — `RecommendationPolicy` |
| `repositories.py` | Implemented — `CaseRepository` protocol |
| `application.py` | Partial — `TriageApplicationService` incomplete |

**Tests (`tests/`):** `test_classification.py`, `test_domain.py`, `test_policy.py`, `test_workflow.py`. The full suite does not yet run: `validate_ticket` and `transition_case` are missing, and persistence, approval, routing, and application tests have not been added.

## Open questions

- Which ticketing platform will be integrated, and does it support webhooks and idempotent updates?
- Which LLM provider and deployment option are approved, and what data may be sent externally?
- What are the approved category taxonomy, priority levels, and routing rules?
- What are the baseline latency, accuracy, availability, and cost targets?
- How should concurrency, transactional persistence, and full audit history be implemented?

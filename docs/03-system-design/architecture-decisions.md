# Architecture Decisions

## ADR-001 — Human Approval Before Routing

**Status:** Proposed

### Context

The system uses an LLM to recommend ticket categories, priorities, and destination teams. Model recommendations may be incorrect.

### Decision

Require an authorized human approval before executing a routing action. The routing component must independently verify approval and the current workflow state.

### Consequences

- Adds a human-review step.
- Requires persistent workflow state.
- Supports auditability and controlled routing.
- Requires handling approval delays and reviewer unavailability.

## ADR-002 — Separate Classification from Business Policy

**Status:** Proposed

### Context

LLMs can interpret ticket text but are not a reliable enforcement mechanism for mandatory business rules.

### Decision

Use the LLM to produce a structured recommendation. Use deterministic application logic to validate the response and enforce routing, priority, and escalation rules.

### Consequences

- Business rules can be tested without calling an LLM.
- Invalid recommendations can be rejected before approval.
- Policy changes can be reviewed independently of prompt changes.
- The system still requires empirical evaluation of classification quality.

## ADR-003 — Begin with a Modular Application

**Status:** Proposed

### Context

The ticket volume estimate alone does not demonstrate a need for microservices or distributed orchestration.

### Decision

Begin with a modular application and clearly defined interfaces. Introduce separate services, queues, or orchestration frameworks only when requirements justify them.

### Consequences

- Reduces initial operational complexity.
- Simplifies local development and testing.
- Keeps future extraction into services possible.
- Requires module boundaries to be maintained deliberately.

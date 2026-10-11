# Sequence Diagram — Ticket Triage Workflow

This diagram documents the normal flow and the key failure paths.

```mermaid
sequenceDiagram
    participant Agent as Support Agent
    participant Ticket as Ticketing Platform
    participant App as Triage Application
    participant Store as Workflow Store
    participant Policy as Policy Engine
    participant LLM as LLM Provider

    Agent->>Ticket: Submit ticket
    Ticket->>App: Ticket received
    App->>App: Validate and normalize
    App->>LLM: Request structured recommendation
    LLM->>App: Category, priority, rationale
    App->>Policy: Validate recommendation
    Policy->>App: Valid recommendation
    App->>Store: Save pending approval
    App->>Agent: Display recommendation

    alt Agent approves
        Agent->>App: Approve recommendation
        App->>Store: Verify approval and status
        App->>Ticket: Execute approved routing
        Ticket->>App: Routing result
        App->>Store: Record outcome
    else Agent corrects or rejects
        Agent->>App: Correct or reject
        App->>Store: Record decision
    else LLM or validation fails
        App->>Store: Record failure
        App->>Agent: Manual review required
    end
```

The diagram introduces a workflow store because approval can happen later than the initial recommendation. The application needs a reliable way to remember the ticket, recommendation, status, and approval decision between those steps.

## Workflow State Machine

A workflow state machine prevents invalid transitions.

```text
RECEIVED
    │
    ▼
PROCESSING
    │
    ▼
PENDING_APPROVAL
    │
    ├──────────────► APPROVED ──► ROUTED
    │
    └──────────────► REJECTED ──► No routing action
```

Errors can transition to `RETRY_PENDING` or `MANUAL_REVIEW`, according to the failure policy.

### Design considerations

- Approval must be associated with the exact recommendation being approved.
- A correction should invalidate the old approval if it changes the proposed action.
- Duplicate approval or routing requests must not cause duplicate side effects.
- A routing timeout can leave the outcome uncertain; reconcile with the ticketing platform before blindly retrying.
- Terminal states and retry transitions should be explicitly defined.

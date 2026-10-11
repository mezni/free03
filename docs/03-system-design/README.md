# Phase 03 — System Design

**Project:** Ticket Triage AI  
**Phase:** 03 — System Design  
**Status:** In Progress  
**Prerequisites:** Discovery and Requirements Engineering

## 1. Purpose

Translate the approved business and technical requirements into a coherent system architecture for the Ticket Triage AI platform.

This phase defines the system boundaries, components, interfaces, data model, runtime interactions, deployment topology, and failure-handling strategies.

The objective is to establish an architecture that is reliable, secure, maintainable, observable, and appropriate for the project's actual requirements.

## 2. Business Context

Support teams receive between an estimated 1,000 and 10,000 tickets per day.

The system aims to reduce manual triage effort by using an LLM to recommend:

- Ticket category
- Ticket priority
- Destination support team
- A concise rationale for the recommendation

A human must approve the recommendation before the system executes the routing action.

The system must validate model output, enforce business rules deterministically, record relevant events, and provide a safe fallback when automated processing fails.

These inputs remain subject to stakeholder validation.

## 3. Architecture Principles

### 3.1 Human-in-the-Loop Control

AI recommendations must not directly trigger routing actions. The application must verify authorization, approval, and workflow state before executing an action.

### 3.2 Separation of Responsibilities

Classification, business policy, approval management, ticketing integration, and audit logging must have clearly defined responsibilities.

### 3.3 Deterministic Business Rules

Mandatory routing, escalation, validation, and authorization rules must be enforced by application logic rather than relying solely on LLM instructions.

### 3.4 Secure by Design

The system must follow least-privilege access, secure credential management, data minimization, and approved data-retention policies.

### 3.5 Resilience and Recoverability

The architecture must account for model timeouts, invalid outputs, API failures, duplicate requests, and uncertain routing outcomes.

### 3.6 Observability

The system must provide appropriate metrics, structured logs, and audit events to support operational monitoring and incident investigation.

### 3.7 Simplicity Before Distribution

Start with a modular application unless measured workload, reliability requirements, or team boundaries justify distributed services.

### 3.8 Replaceable Dependencies

Model providers and ticketing integrations should be isolated behind interfaces to reduce vendor coupling.

## 4. Scope

### In Scope

- Ticket ingestion and normalization
- LLM-based classification recommendations
- Structured-output validation
- Deterministic routing and escalation policies
- Human approval workflow
- Approval-gated routing
- Workflow state persistence
- Ticketing platform integration
- Audit logging and operational monitoring
- Retry, reconciliation, and manual fallback behavior

### Out of Scope for the Initial MVP

Unless discovery identifies a justified requirement, the initial release excludes:

- Autonomous routing without human approval
- Automatic customer replies
- Automatic ticket resolution or closure
- Multi-agent orchestration
- A vector database or retrieval pipeline without a demonstrated need
- Microservices introduced solely for architectural complexity

## 5. Logical Architecture

The initial logical architecture contains the following components:

| Component | Responsibility |
|---|---|
| Ticketing Platform | Source of tickets and destination for approved routing updates |
| Ingestion Layer | Receives and validates incoming ticket events |
| Normalization Layer | Converts external ticket data into an internal representation |
| Classification Service | Requests structured recommendations from an LLM |
| Policy Engine | Validates recommendations and applies deterministic business rules |
| Approval Workflow | Manages review, approval, correction, and rejection |
| Workflow Store | Persists ticket processing state and approval status |
| Routing Adapter | Executes approved routing actions through the ticketing platform |
| Audit and Monitoring | Records relevant events, failures, and operational metrics |

These are logical responsibilities, not necessarily separate deployable services.

## 6. Documents and Deliverables

| Document | Purpose | Status |
|---|---|---|
| `README.md` | Phase objectives, scope, principles, and deliverables | Current |
| `system-context.md` | External actors, systems, and system boundaries | Planned |
| `container-diagram.md` | Runtime components and their relationships | Planned |
| `sequence-diagram.md` | Interaction flows and failure paths | Drafted |
| `data-model.md` | Core entities, relationships, and workflow state | Planned |
| `api-contracts.md` | Internal interfaces and external integration contracts | Planned |
| `architecture-decisions.md` | Architecture Decision Records (ADRs) | Drafted |
| `deployment-architecture.md` | Deployment topology and operational environment | Planned |
| `failure-handling.md` | Timeouts, retries, idempotency, reconciliation, and fallback | Planned |

All planned deliverables require review and validation before the architecture is considered approved.

## 7. Key Architecture Questions

The following decisions must be informed by requirements and evidence rather than assumptions.

### Integration

- Which ticketing platform will be integrated?
- Does it support APIs, webhooks, and idempotent updates?
- What rate limits and authorization mechanisms apply?

### Model Inference

- Which model provider and deployment option are approved?
- What structured-output capabilities are available?
- What are the latency, cost, and data-handling constraints?

### Persistence

- Which workflow states must survive application restarts?
- How will duplicate events and concurrent approvals be handled?
- What audit retention requirements apply?

### Scalability

- What are the measured peak ticket arrival rates?
- What are the required throughput and latency targets?
- Are asynchronous workers or a queue necessary?

### Security and Privacy

- Which ticket fields may be sent to the model?
- What access controls are required?
- Where may data be processed and stored?

## 8. Architecture Decision Records

Architecture decisions should be documented with context, the selected decision, alternatives considered, and consequences.

Initial proposed decisions:

- **ADR-001:** Require human approval before routing.
- **ADR-002:** Separate LLM classification from deterministic business policy.
- **ADR-003:** Begin with a modular application.
- **ADR-004:** Define safe retry, idempotency, and reconciliation behavior for routing actions.

Decisions remain provisional until their assumptions and trade-offs have been reviewed.

## 9. Validation and Verification Strategy

The architecture must support verification at several levels:

- **Unit tests:** Validate normalization, policy rules, state transitions, and output validation.
- **Integration tests:** Verify model and ticketing adapters using controlled test environments.
- **Workflow tests:** Verify approval, rejection, correction, and authorization behavior.
- **Failure tests:** Simulate timeouts, retries, duplicate requests, and uncertain routing outcomes.
- **Evaluation tests:** Measure category quality, routing accuracy, priority agreement, and urgent-ticket errors.
- **Load tests:** Validate performance against measured workload and approved targets.
- **Security tests:** Verify access control, secret handling, and protection against unauthorized actions.

## 10. Exit Criteria

System Design is complete when:

- [ ] System boundaries and external dependencies are documented.
- [ ] Component responsibilities and interfaces are defined.
- [ ] Ticket, recommendation, approval, and audit data models are specified.
- [ ] The main workflow and critical failure paths are documented.
- [ ] Human approval is enforced independently of model output.
- [ ] Persistence, retry, idempotency, and reconciliation behavior are specified.
- [ ] Security, privacy, observability, and deployment requirements are addressed.
- [ ] Architecture decisions and their trade-offs are recorded.
- [ ] The design can be traced back to approved requirements.
- [ ] Stakeholders have reviewed and approved the architecture baseline.

## 11. Next Phase

**Phase 04 — Implementation and Engineering Foundations**

Implementation should begin only after the architecture is sufficiently defined to support clear module boundaries, testable interfaces, safe workflow behavior, and a justified initial technology stack.

The first implementation milestone should be a small, testable vertical slice rather than a complete distributed platform.

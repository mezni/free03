# 01 — Discovery

## Overview

This phase establishes the business context, problem statement, stakeholder needs, constraints, and success criteria for the AI-powered ticket triage system.

The goal is to understand the problem before selecting an AI model, framework, or infrastructure.

## Business Objective

Reduce the time support agents spend manually triaging incoming tickets while maintaining or improving classification and routing quality.

## Project Context

The proposed system analyzes incoming support tickets and recommends:

- Ticket category and subcategory
- Priority and urgency
- Responsible support team
- A concise ticket summary
- Missing information or reasons for escalation

The initial operating model requires a human to review and approve recommendations before the corresponding routing action is executed.

## Initial Project Inputs

| Attribute | Initial Value |
|---|---|
| Project name | `ticket-triage` |
| Expected volume | 1,000–10,000 tickets per day |
| Primary objective | Reduce manual triage time |
| Automation model | AI recommendation followed by human approval |
| Ticketing platform | Not yet identified |
| Technical constraints | To be established |
| Security and privacy requirements | To be established |

These inputs represent the initial project assumptions and constraints. They must be validated during stakeholder discovery.

## Discovery Objectives

1. Understand the current ticket triage workflow.
2. Identify operational bottlenecks and failure points.
3. Establish the current performance baseline.
4. Identify stakeholders and their responsibilities.
5. Define the initial project scope and boundaries.
6. Discover integration, security, privacy, and infrastructure constraints.
7. Establish measurable success criteria.
8. Identify unresolved questions and risks.

## Deliverables

| Document | Purpose |
|---|---|
| `discovery-brief.md` | Summarizes the business problem, objectives, scope, and risks |
| `stakeholder-interviews.md` | Defines interview questions and captures stakeholder findings |
| `assumptions-and-constraints.md` | Tracks assumptions, confirmed facts, constraints, and open questions |
| `success-metrics.md` | Defines performance metrics, baselines, targets, and evaluation methods |

## Stakeholders

| Stakeholder | Primary Responsibility |
|---|---|
| Support manager | Business workflow, KPIs, SLAs, and operational needs |
| Support agents | Practical triage decisions, exceptions, and usability |
| Product owner | Scope, priorities, and acceptance criteria |
| IT / platform engineering | APIs, integration, infrastructure, and reliability |
| Security / privacy | Data handling, access control, and audit requirements |

## Initial Success Criteria

The following are proposed pilot targets, pending stakeholder approval:

- Reduce median triage time by at least 30%.
- Achieve at least 95% routing accuracy on an agreed evaluation dataset.
- Achieve at least 95% agreement with approved priority labels.
- Achieve at least 85% unmodified human acceptance of recommendations.
- Maintain complete coverage of required human approvals.
- Maintain complete traceability of recommendations and approval decisions.

Targets must be validated against the baseline, ticket distribution, and business risk. Measurement definitions and evaluation datasets must be agreed before the pilot.

## Scope Boundaries

### In Scope

- Ticket classification
- Priority and routing recommendations
- Human review and approval
- Decision logging
- Evaluation of classification and routing quality

### Initially Out of Scope

- Autonomous customer replies
- Autonomous refunds or account changes
- Unreviewed autonomous routing
- Replacing the existing ticketing platform
- Multi-agent orchestration without a demonstrated requirement

Scope boundaries remain subject to stakeholder approval.

## Key Discovery Questions

- Which ticketing platform is currently used?
- What are the ticket categories and routing rules?
- What is the current median and 95th-percentile triage time?
- What is the existing routing accuracy?
- What historical ticket data is available?
- What latency and availability requirements apply?
- What data may be sent to an external LLM provider?
- Which decisions must always require human review?
- What budget and operating-cost limits apply?

## Exit Criteria

The Discovery phase is complete when:

- [ ] The business problem and primary objective are documented.
- [ ] Relevant stakeholders have been interviewed.
- [ ] The current workflow and baseline metrics are documented or their data gaps are explicitly recorded.
- [ ] Initial scope boundaries have been reviewed.
- [ ] Assumptions, constraints, and open questions are tracked.
- [ ] Success metrics and evaluation methods are proposed and reviewed.
- [ ] Stakeholders agree to proceed to requirements engineering.

## Next Phase

**Phase 02 — Requirements Engineering**

The next phase converts discovery findings into business requirements, functional requirements, nonfunctional requirements, use cases, acceptance criteria, and a prioritized requirements backlog.

Architecture and technology decisions will be grounded in these requirements rather than made prematurely.

# Experiment 11 — Multi-Agent Handoff

## Goal

Introduce explicit coordination between specialized agents.

## Agents

### Research Agent

Responsible for:

- searching historical tickets
- identifying similar cases
- reporting previous resolutions

It cannot:

- create tickets
- escalate tickets
- modify customer accounts
- make final support decisions

### Support Agent

Responsible for:

- customer-facing response
- knowledge-base search
- ticket creation
- escalation

It does not search historical tickets directly.

## Handoff Contract

The orchestrator creates:

- `ResearchRequest` (ticket_id, customer_id, issue_summary, category, urgency, product, priority, research_question)

The research agent returns:

- `ResearchResult` (ticket_id, findings, similar_tickets)

## Context Loss Experiment

The first design passed only a research question.

This lost:

- ticket ID
- customer ID
- category
- urgency
- product
- priority

The problem was fixed with an explicit Pydantic handoff model.

## Redundant Tool Call Experiment

Initially, the support agent could access:

- `search_similar_tickets`

This allowed it to repeat work performed by the research agent.

The solution was to create agent-specific tool sets.

## Loop Prevention

The orchestrator controls the workflow.

The architecture is:

Support
    ↓
Research
    ↓
Support

The research agent cannot invoke the support agent.

The support agent cannot invoke the research agent.

Therefore the workflow has a single controlled handoff.

## Architecture

Customer
    ↓
Extraction
    ↓
Triage
    ↓
Orchestrator
    ├── Research Agent
    │     └── Historical Search
    │
    └── Support Agent
          ├── Knowledge Base
          ├── Create Ticket
          └── Escalate

## Lessons

1. Agent communication should use explicit contracts.
2. Context should be deliberately selected.
3. Agents should receive only the tools they need.
4. Application code should control workflow boundaries.
5. Multi-agent systems increase coordination complexity.
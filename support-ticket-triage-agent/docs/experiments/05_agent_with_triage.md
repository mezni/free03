# Experiment 05 — Agent with Triage Context

## Objective

Connect structured extraction, triage, and the agent loop.

## Pipeline

SupportTicket
    ↓
Extraction
    ↓
TicketExtraction
    ↓
Triage
    ↓
TriageDecision
    ↓
Agent
    ↓
Claude
    ↓
Tool
    ↓
Final response

## Agent Inputs

The agent receives:

- original ticket
- extracted information
- triage decision

## Tool

knowledge_base_search

## Observations

- whether the model used the tool
- what query it generated
- whether the query was useful
- whether the tool was needed
- whether the final response used the retrieved information
- whether the triage decision influenced the behavior

Recorded observations from the live run (T001–T006):

- The agent's first turn begins with an acknowledgment text block and a
  `tool_use` block; the loop currently returns on the first text block, so
  the tool call is never executed and the final response is just the
  preamble.
- All five populated tickets (T001–T005) produced preamble responses that
  announced a knowledge-base search without performing one.
- T006 (empty ticket, low urgency, no knowledge search, no escalation) was
  responded to without a tool call, and the agent asked for the missing
  ticket content — triage context was used.

## Important Lesson

Extraction, triage, and execution are separate responsibilities.

Extraction determines what information is present.

Triage determines how the ticket should be handled.

The agent determines which available actions are necessary.

The application executes the requested tools.

## Follow-up

The loop must not treat the first text block as the final response when a
`tool_use` block follows it in the same message. The agent should run the
tool first and only emit text after all tool calls in the turn are resolved.
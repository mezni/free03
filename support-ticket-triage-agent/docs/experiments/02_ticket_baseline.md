# Experiment 02 — Support Ticket Baseline

## Objective

Create a baseline LLM application that processes support tickets.

## Input

A SupportTicket containing:

- ticket ID
- customer ID
- subject
- message

## Output

A TriageResult containing:

- category
- urgency
- drafted response

## Categories

- billing
- technical_support
- account
- shipping
- security
- other

## Urgency

- low
- medium
- high
- critical

## Tools

None.

## Memory

None.

## Agent loop

None.

## Observations

The model can perform basic ticket classification and response
generation in a single LLM call.

This implementation is still a standard LLM application rather
than an agentic system.
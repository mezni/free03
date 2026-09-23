# Experiment 02 — Structured Ticket Extraction

## Objective

Extract structured information from support tickets.

## Input

Free-form support ticket.

## Output

TicketExtraction:

- customer_id
- product
- sentiment
- priority

## Validation

Pydantic validates the model output.

## Failure cases

We deliberately test:

- missing customer ID
- empty subject
- empty body
- ambiguous product
- unexpected product
- malformed JSON
- missing fields

## Important observations

There are two major classes of model-output failure:

1. JSON parsing failure
2. Schema validation failure

These will later require explicit recovery strategies.
# Experiment 13 — Evaluation

## Goal

Measure agent behavior systematically instead of
relying on manual inspection.

## Evaluation dimensions

### Extraction

Evaluate:

- product
- priority
- customer ID
- sentiment

### Triage

Evaluate:

- category
- urgency
- escalation

### Research

Evaluate:

- relevant historical cases
- useful findings
- absence of fabricated cases

### Tool behavior

Evaluate:

- selected tool
- tool arguments
- number of calls
- tool failures

### Final response

Evaluate:

- addresses the issue
- avoids fabricated information
- follows business rules
- professional response

## Deterministic evaluation

Use exact comparisons where possible.

Examples:

category == expected_category

priority == expected_priority

## Semantic evaluation

Use criteria-based or LLM-based evaluation
only when exact comparison is inappropriate.

## Regression testing

Every system change should be evaluated against
the fixed dataset.

A change is not considered an improvement merely
because one example looks better.

## Important lesson

Evaluation converts an agent from:

"I think it works"

into:

"We have measurements showing how it behaves."
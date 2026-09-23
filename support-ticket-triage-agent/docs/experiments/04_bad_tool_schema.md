# Experiment 04 — Deliberately Bad Tool Schema

## Objective

Understand how an ambiguous tool schema affects model tool usage.

## Tool

The actual Python function is:

knowledge_base_search(query: str)

## Deliberately Bad Schema

The model sees:

- tool name: search
- parameter: input
- description: Search stuff.

## Problems

The schema does not clearly communicate:

- what is being searched
- when the tool should be used
- what the input parameter represents
- what kind of query should be supplied

## Observed Behavior

Record the actual tool request produced by the model.

Example:

```text
Tool:
search

Input:
{
    "input": "internet problem"
}
# ADR-002: PostgreSQL + pgvector

## Decision

Use PostgreSQL with pgvector for persistence and vector search.

## Reason

It provides:

- relational persistence
- metadata filtering
- transactions
- vector similarity search
- a single primary database for the initial product
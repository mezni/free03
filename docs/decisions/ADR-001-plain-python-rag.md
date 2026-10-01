# ADR-001: Plain Python RAG Architecture

## Decision

Use plain Python abstractions and services rather than a RAG framework.

## Reason

The project is intended to expose the internal mechanics of a RAG system:

- retrieval
- indexing
- prompting
- evaluation
- provider abstraction
- observability
- reliability

Frameworks may be introduced later if a concrete requirement justifies them.
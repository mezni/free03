# ADR-004: Provider Abstraction

## Decision

LLM and embedding providers are accessed through application-defined interfaces.

## Reason

The application should not be tightly coupled to one model provider.

This also allows deterministic providers to be used in tests.
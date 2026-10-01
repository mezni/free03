# Architecture Overview

## Architectural Style

RAG System uses a layered object-oriented architecture.

## Layers

### API

Responsible for:

- HTTP requests
- authentication
- validation
- error mapping

### Application

Responsible for:

- service composition
- use-case orchestration

### Services

Responsible for:

- ingestion
- indexing
- retrieval
- generation
- evaluation
- observability
- FinOps

### Domain/Application Models

Pydantic models define application contracts.

### Persistence

SQLAlchemy models and repositories provide database access.

### Providers

External infrastructure is isolated behind provider interfaces.

Examples:

- embedding provider
- LLM provider

### Infrastructure

- PostgreSQL
- pgvector
- OpenRouter
- Docker

## Dependency Direction

API
  ↓
Application Services
  ↓
Repositories / Providers
  ↓
Infrastructure

Business/application code should not depend directly on HTTP implementation details.
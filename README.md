# rag-system

Enterprise Knowledge RAG API

## Overview

Enterprise knowledge retrieval and question-answering platform. Allows applications to ingest organizational documents and answer questions using those documents with source citations.

## Features

- Document ingestion (discover, parse, clean, chunk, embed, index)
- Change detection and incremental processing
- Vector, keyword, and hybrid retrieval
- Reranking and context expansion
- LLM answer generation with citations
- Index versioning (BUILDING → ACTIVE → RETIRED)
- Retrieval and RAG evaluation
- Observability and cost tracking
- API authentication and health checks

## Architecture

Layered object-oriented architecture with separation of concerns:

- **API** – HTTP requests, authentication, validation, error mapping
- **Application** – service composition, use-case orchestration
- **Services** – ingestion, indexing, retrieval, generation, evaluation, observability, FinOps
- **Domain Models** – Pydantic models defining application contracts
- **Persistence** – SQLAlchemy models and repositories
- **Providers** – external infrastructure (embedding, LLM) behind interfaces
- **Infrastructure** – PostgreSQL with pgvector, OpenRouter, Docker

## Product Workflows

### Workflow A — Ingestion
Documents → Discover → Change Detection → Load → Parse → Clean → Metadata → Chunk → Embed → Index → Document becomes ACTIVE

### Workflow B — Question answering
User Question → API → Query Analysis → Retrieval → Reranking → Context Selection → LLM → Citation Extraction → Grounding Validation → RAGResponse

### Workflow C — Reindex
Existing ACTIVE index → Create BUILDING index → Process documents → Generate embeddings → Validate → Activate new index → Retire previous index

## Technology Stack

- Python >= 3.12
- FastAPI
- PostgreSQL with pgvector
- OpenRouter LLM provider
- Alembic for migrations
- uv for packaging
- ruff for linting
- mypy for type checking
- pytest for testing

## Quick Start

```bash
cp .env.example .env
docker compose up -d
uv sync
uv run alembic upgrade head
uv run uvicorn src.api.app:create_app --factory --reload
```

## Configuration

Environment variables via `.env` file and YAML settings in `src/config/`. Key settings include database connection, embedding provider, LLM provider, chunking parameters, and retrieval configuration.

## API

- `GET /health` – reports liveness
- `GET /health/ready` – verifies database readiness
- `POST /rag/query` – accepts a question and returns an answer with citations

## Ingestion

Documents are discovered from the filesystem, processed through a pipeline (load, parse, clean, extract metadata, chunk, embed), and indexed into PostgreSQL/pgvector. Change detection ensures incremental updates. New documents become ACTIVE; modified documents are reprocessed; unchanged documents are skipped.

## Retrieval

Queries search only the ACTIVE index. Supports vector search, keyword search, and hybrid search with metadata filtering. Results can be reranked and context can be expanded. Answers contain citations when supporting sources exist.

## Evaluation

Retrieval metrics (recall@k, precision@k, MRR, nDCG@k) and RAG answer metrics can be calculated. Quality gates can fail CI when configured thresholds are not met. Evaluation datasets and results are persisted for regression tracking.

## Observability

Requests have correlation IDs. Retrieval and generation operations are measured. LLM usage is tracked. Audit events can be persisted for compliance.

## Reliability

Transient provider failures can be retried with backoff. Circuit breaker prevents repeated calls to an unavailable provider. Request timeouts are enforced. Errors contain a request ID; internal implementation details are not exposed.

## FinOps

Cost tracking for LLM token usage and embedding generation. Metrics are persisted and can be queried for optimization.

## Production Deployment

Docker-based deployment with docker-compose for development and docker-compose.prod.yml for production. Health checks and readiness endpoints are available. Migrations are run via `alembic upgrade head`.

## Development

```bash
uv run pytest        # Run tests
uv run ruff check .  # Lint
uv run mypy src      # Type check
```

## Testing

Unit tests and integration tests are available. Evaluation can be run via `src.cli.evaluate` and `src.cli.evaluate_rag`. All tests must pass before deployment.

## Known Limitations

- Initial product does not support authentication providers (OAuth/OIDC)
- No multi-tenancy
- No web crawling
- No autonomous agents
- Single-primary database architecture

## Roadmap

- Phase 1: Core ingestion, retrieval, and generation
- Phase 2: Advanced retrieval (reranking, context expansion)
- Phase 3: Evaluation and quality gates
- Phase 4: Cost tracking and FinOps
- Phase 5: Production hardening and deployment automation
# Component Reference

## API Layer

### Routes

- `src/api/routes/health.py` – `/health` and `/health/ready` endpoints
- `src/api/routes/rag.py` – `/rag/query` endpoint
- `src/api/routes/metrics.py` – metrics collection endpoints
- `src/api/routes/__init.py` – route registration

### Middleware

- `src/api/middleware/security_headers.py` – HTTP security headers
- `src/api/middleware/timeout.py` – request timeout enforcement
- `src/api/middleware/rate_limit.py` – rate limiting

### Error Handling

- `src/api/errors.py` – error response formatting
- `src/core/errors.py` – base exception types
- `src/core/exceptions.py` – domain-specific exceptions

## Application Layer

### Service Container

- `src/application/container.py` – dependency injection container

### Core Services

- `src/services/document_service.py` – document lifecycle management
- `src/services/ingestion_run_service.py` – ingestion run orchestration
- `src/services/indexing_service.py` – indexing operations
- `src/services/reindex_service.py` – reindex workflow (BUILDING→ACTIVE)
- `src/services/versioning_service.py` – index version management (BUILDING/ACTIVE/RETIRED/FAILED)
- `src/services/retrieval_service.py` – query processing and retrieval
- `src/services/generation_service.py` – LLM-backed answer generation
- `src/services/grounding_service.py` – grounding/citation validation
- `src/services/evaluation_resolver.py` – evaluation result processing
- `src/services/retrieval_metrics_service.py` – retrieval metric calculation
- `src/services/retrieval_evaluation_service.py` – RAG evaluation orchestration
- `src/services/reindex_service.py` – reindex service
- `src/services/document_processing_service.py` – document processing pipeline

### Models

- `src/models/` – Pydantic application/domain models
  - `Document`, `DocumentCreate`
  - `IngestionRun`, `IngestionRunStatus`
  - `DocumentProcessingResult`, `DocumentProcessingStatus`
  - `IndexValidationResult`
  - `RetrievalQuery`, `RetrievalResult`
  - `GenerationRequest`, `GenerationResponse`
  - `Citation`, `RAGResponse`

## Domain Layer

### Core Primitives

- `src/core/ids.py` – ID generation (ULID-based)
- `src/core/clock.py` – timezone-aware clock
- `src/core/enums.py` – DocumentChangeType, DocumentLifecycleStatus, IndexVersionStatus, etc.
- `src/core/hashing.py` – content hashing utilities

### Repository Pattern

- `src/db/repositories/` – SQLAlchemy-based repositories
  - `documents.py` – Document repository
  - `chunks.py` – Chunk repository (version-scoped)
  - `embeddings.py` – Embedding repository
  - `index_versions.py` – Index version repository
  - `documents_processing.py` – Document processing history
  - `vector_search.py` – Vector search operations
  - `keyword_search.py` – Keyword search operations
  - `runs.py` – Ingestion run repository
  - `llm_usage.py` – LLM usage tracking
  - `audit.py` – Audit event repository

### Embedding Providers

- `src/providers/embeddings/base.py` – EmbeddingProvider base interface
- `src/providers/embeddings/local.py` – LocalEmbeddingProvider (SHA-256 stub)
- `src/providers/embeddings/factory.py` – Embedding provider factory

### LLM Providers

- `src/providers/llm/base.py` – LLMProvider base interface
- `src/providers/llm/openrouter.py` – OpenRouter provider implementation
- `src/providers/llm/factory.py` – LLM provider factory

## Infrastructure

- PostgreSQL with pgvector extension
- Alembic migration management
- Docker container orchestration
- Environment configuration via .env + YAML
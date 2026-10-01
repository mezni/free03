# rag-system — Project Handoff / Current State

## 1. Project goal

We are building a production-oriented RAG platform step by step, primarily as a learning project.

The project name is:

```
rag-system
```

The goal is to learn and implement:

```
Document ingestion
→ Chunking
→ Embeddings
→ Vector indexing
→ Retrieval
→ LLM generation
→ Guardrails
→ Evaluation
→ Observability
→ RAGOps
→ FinOps
→ API
→ CLI
→ Streamlit
→ CI/CD
→ Production hardening
```

Implementation preferences:

- Python 3.12 (`pyproject.toml` says `requires-python = ">=3.12"`; the venv is
  3.12.13 — earlier notes said 3.13, which is wrong)
- `uv` for dependency/project management
- Pydantic/Pydantic Settings for application models and configuration
- SQLAlchemy for persistence
- Alembic for migrations
- PostgreSQL + pgvector
- Docker Compose
- OOP style
- Not DDD
- Build incrementally: one step at a time
- When I say "next", give me the next implementation step, not the entire roadmap.
- `.env` should stay small: secrets/environment-specific values only.
- YAML should contain application/model/pipeline configuration.

## 2. High-level architecture

Current architecture:

```
                         ┌──────────────────┐
                         │   Data Sources   │
                         │ filesystem/API/  │
                         │      RDBMS       │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │    Ingestion     │
                         │                  │
                         │ Discovery        │
                         │ Change Detection │
                         │ Loading          │
                         │ Parsing          │
                         │ Cleaning         │
                         │ Metadata         │
                         │ Chunking         │
                         │ Embedding        │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │    Indexing      │
                         │                  │
                         │ ADD              │
                         │ UPDATE           │
                         │ DELETE           │
                         │ REINDEX          │
                         └────────┬─────────┘
                                  │
                                  ▼
                    ┌──────────────────────────┐
                    │ PostgreSQL + pgvector    │
                    │                          │
                    │ documents                │
                    │ chunks                   │
                    │ embeddings               │
                    │ index_versions           │
                    │ ingestion_runs           │
                    │ document_processing      │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                         ┌──────────────────┐
                         │    Retrieval     │
                         │ vector/hybrid    │
                         │ filtering        │
                         │ reranking        │
                         │ context building │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │    Generation    │
                         │ prompts          │
                         │ guardrails       │
                         │ LLM              │
                         │ citations        │
                         └────────┬─────────┘
                                  │
                                  ▼
                              Answer
```

Cross-cutting:

- RAGOps
- Observability
- Evaluation
- FinOps (partial)
- Versioning
- Security
- CI/CD (not started)

Request path today:

```
POST /rag/query
   ↓
RAGService.answer()
   ↓
RetrievalPipeline.execute()        metrics, timing, rerank
   ↓
RetrievalService.search()          resolve ACTIVE version, embed, dimension check
   ↓
SearchStrategy                     vector | keyword | hybrid(RRF)
   ↓
GenerationService.generate()       prompt + [SOURCE-n] markers
   ↓
LLMProvider (OpenRouter)
   ↓
CitationExtractor + GroundingService
   ↓
RAGResponse (answer + citations)
```

## 3. Project foundation — FINISHED

We created the project with `uv`.

Current technology stack:

- Python 3.12
- uv
- Pydantic / pydantic-settings
- PyYAML
- python-dotenv
- FastAPI + uvicorn + httpx
- pytest / ruff / mypy (+ `types-pyyaml`, `pytest-cov`)
- SQLAlchemy / psycopg / Alembic / pgvector

Basic project configuration is in place.

`.env.example` is intentionally small:

```
APP_ENV=dev
DATABASE_URL=postgresql+psycopg://rag:rag_dev_password@localhost:5432/rag_system
OPENROUTER_API_KEY=
```

`.gitignore` also excludes `.env.*` while keeping `.env.example` tracked.

Configuration is separated:

```
.env
    ↓
secrets/environment-specific values
(APP_ENV, DATABASE_URL, OPENROUTER_API_KEY)

config/*.yaml
    ↓
application/model/pipeline configuration
(settings, embedding, llm, ingestion, reliability)
```

## 4. Docker + PostgreSQL — FINISHED

Docker Compose is configured with:

```
image: pgvector/pgvector:pg17
```

Database:

- database: `rag_system`
- user: `rag`
- password: `rag_dev_password`
- port: `5432`

We have:

- `docker-compose.yml`

with:

- PostgreSQL
- pgvector
- persistent volume
- healthcheck

Makefile includes database/container commands such as:

- `make up`
- `make down`
- `make ps`
- `make logs`
- `make db-shell`

## 5. SQLAlchemy + Alembic — FINISHED

Configured:

- `src/db/base.py`
- `src/db/engine.py`
- `src/db/session.py`
- `migrations/`
- `alembic.ini`

Alembic is working.

We have already created and applied multiple migrations.

Important architecture:

```
Pydantic models
      ↓
Application/domain data

SQLAlchemy models
      ↓
Database persistence

Repository
      ↓
Database access

Service
      ↓
Transaction/application orchestration
```

Repositories generally `flush()` but don't own the overall transaction.

Services generally own commits/rollbacks.

## 6. Document model — FINISHED

We have a Pydantic document model:

`src/models/document.py`

It contains:

- `DocumentCreate`
- `Document`

Fields include:

- `id`
- `source`
- `source_uri`
- `title`
- `content_hash`
- `status`
- `created_at`
- `updated_at`

Content hashes use SHA-256.

## 7. Document database model — FINISHED

We have:

`src/db/models/document.py`

with:

`documents`

Database fields include:

- `id`
- `source`
- `source_uri`
- `title`
- `content_hash`
- `status`
- `created_at`
- `updated_at`

## 8. Document Repository — FINISHED

We created:

`src/db/repositories/documents.py`

Capabilities include:

- `create()`
- `get_by_id()`
- `get_by_source_uri()`
- `get_by_content_hash()`
- `delete()`
- `update_content_hash()`
- `update_status()`

There is also mapping from SQLAlchemy model → Pydantic model.

## 9. Document Service — FINISHED

Created:

`src/services/document_service.py`

Responsibilities:

- `create_document()`
- `get_document()`
- `get_by_source_uri()`
- `delete_document()`
- `set_processing()`
- `set_active()`
- `set_failed()`

The service owns transaction boundaries for these operations.

## 10. Ingestion pipeline — FINISHED through the embedding stage

The ingestion architecture is:

```
Discovery
    ↓
Change Detection
    ↓
Loading
    ↓
Parsing
    ↓
Cleaning
    ↓
Metadata Extraction
    ↓
Chunking
    ↓
Embedding
    ↓
Indexing
```

## 11. Filesystem discovery — FINISHED

Created:

- `src/ingestion/sources/base.py`
- `src/ingestion/sources/filesystem.py`
- `src/ingestion/stages/discover.py`

Filesystem currently supports:

- `*.md`
- `*.txt`

The earlier source implementation also had PDF support in its pattern list, but PDF ingestion is not implemented yet, so the current pipeline factory intentionally uses only:

```python
patterns=("*.md", "*.txt")
```

## 12. Change detection — FINISHED

We created:

- `src/core/hashing.py`
- `src/core/enums.py`
- `src/ingestion/change_detection.py`

Change types:

- `NEW`
- `MODIFIED`
- `UNCHANGED`

Detection is based on SHA-256 content hashes.

Architecture:

```
file
 ↓
SHA-256
 ↓
compare with stored hash
 ↓
NEW / MODIFIED / UNCHANGED
```

The detector itself does not query the database. The application/service layer provides the previous hash.

## 13. Loading — FINISHED

Created:

`src/ingestion/loaders/`

with the loader abstraction and filesystem implementation.

Current filesystem loader:

- UTF-8 text

producing:

- `RawDocument`

## 14. Parsing — FINISHED

Created parser abstraction and registry.

Current parsers:

- `MarkdownParser`
- `TextParser`

Supported:

- `.md`
- `.markdown`
- `.txt`

The registry chooses the parser based on file extension.

PDF parser is not implemented yet.

## 15. Cleaning — FINISHED

Created:

- `CleanedDocument`
- `DocumentCleaner`
- `TextDocumentCleaner`
- `CleanStage`

Current cleaning includes:

- normalize line endings
- remove trailing whitespace
- collapse excessive blank lines
- strip surrounding whitespace

Important:

The original `content_hash` remains the source-file hash, not a hash of cleaned content.

## 16. Metadata extraction — FINISHED

Created:

- `DocumentMetadata`
- `EnrichedDocument`
- `MetadataExtractor`
- `FilesystemMetadataExtractor`
- `EnrichStage`

Metadata includes:

- `source`
- `source_uri`
- `file_name`
- `extension`
- `document_type`
- `title`
- `file_size_bytes`
- `modified_at`

Markdown title extraction currently looks for:

- `# Title`

## 17. Chunking — FINISHED

Created:

- `DocumentChunk`
- `ChunkedDocument`
- `DocumentChunker`
- `CharacterTextChunker`
- `ChunkStage`

Current learning defaults:

```
chunk_size = 500
chunk_overlap = 50
```

Chunks contain:

- `chunk_id`
- `document`
- `content`
- `content_hash`
- `chunk_index`
- `start_char`
- `end_char`
- `metadata`

The current chunker is a simple character-based chunker.

This is not yet the final RAG chunking strategy.

Later we will evaluate chunking using:

- Recall@K
- MRR
- NDCG
- context relevance

## 18. Embedding — FINISHED for development

Created:

- `src/embeddings/base.py`
- `src/embeddings/local.py`

Models:

- `ChunkEmbedding`
- `EmbeddedDocument`

Embedding abstraction:

- `EmbeddingProvider`

Current development provider:

- `LocalEmbeddingProvider`

It produces deterministic 8-dimensional vectors.

Important:

This is a development/testing embedding provider, not a production semantic embedding model.

Later we will support real providers such as OpenAI/Voyage/local models.

## 19. pgvector — FINISHED

PostgreSQL now uses:

```
pgvector/pgvector:pg17
```

The vector extension is enabled through Alembic.

Database model:

`embeddings`

contains:

- `chunk_id`
- `model_name`
- `dimensions`
- `vector`
- `created_at`

Current vector dimension:

```
8
```

This is intentionally temporary for the local embedding provider.

Later this becomes configuration-driven.

## 20. Chunk + embedding database persistence — FINISHED

Created:

- `src/db/models/chunk.py`
- `src/db/models/embedding.py`
- `src/db/repositories/chunks.py`
- `src/db/repositories/embeddings.py`

Database:

```
documents
    │
    └── chunks
           │
           └── embeddings
```

Foreign keys and cascade behavior are configured.

## 21. End-to-end ingestion — FINISHED

The filesystem ingestion pipeline now runs:

```
file
 ↓
discovery
 ↓
change detection
 ↓
loading
 ↓
parsing
 ↓
cleaning
 ↓
metadata
 ↓
chunking
 ↓
embedding
 ↓
indexing
```

Behavior:

```
NEW
 ↓
ADD

MODIFIED
 ↓
UPDATE

UNCHANGED
 ↓
SKIP
```

Integration tests verify ingestion.

## 22. Indexing Service — FINISHED

Created:

`src/services/indexing_service.py`

Supported operations:

- ADD
- UPDATE
- DELETE
- REINDEX

Model:

- `IndexRequest`

Indexing Service handles:

- document creation
- chunk persistence
- embedding persistence
- document update
- chunk replacement
- document deletion
- transaction rollback

## 23. Index versioning — FINISHED

We introduced:

`index_versions`

with:

- `version_number`
- `status`
- `embedding_model`
- `embedding_dimensions`
- `created_at`
- `activated_at`

Statuses:

- BUILDING
- ACTIVE
- RETIRED
- FAILED

Every chunk now has:

`index_version_id`

This allows multiple index versions to coexist.

Architecture:

```
Index Version 1
    ↓
chunks + embeddings

Index Version 2
    ↓
chunks + embeddings
```

This is the foundation for zero/low-downtime index rebuilding.

## 24. Versioning Service — FINISHED

Created:

`src/services/versioning_service.py`

Capabilities:

- `create_version()`
- `activate_version()`
- `fail_version()`
- `get_active_version()`
- `get_version()` (domain model lookup; static `to_domain()` maps `IndexVersionDB` → Pydantic `IndexVersion`)

Index version repository supports:

- `create_building()`
- `get_active()`
- `get_by_id()`
- `get_by_version_number()`
- `get_next_version_number()`
- `activate()`
- `mark_failed()`

## 25. Reindex Service — FINISHED

Created:

`src/services/reindex_service.py`

Current workflow (`reindex(embedding_model, embedding_dimensions) -> IndexVersion`):

```
create BUILDING version
        ↓
_build_version: discover source → run PipelineStages
   load → parse → clean → enrich → chunk → embed
        ↓
add each document into the BUILDING version (IndexingService.add_to_version)
        ↓
validate (IndexValidationService — chunk/embedding counts, dimensions,
duplicates, missing embeddings, non-empty guarantee)
        ↓
valid? ──no──► mark version FAILED (rollback + re-persist + commit) → raise
  │yes
  ▼
activate version (retires previous ACTIVE) → commit → return IndexVersion
```

The constructor injects `VersioningService`, `IndexingService`,
`IndexValidationService`, and the ingestion components (`document_source`,
`document_loader`, `parser_registry`, `cleaner`, `metadata_extractor`,
`chunker`, `embedding_provider`). It builds the existing `PipelineStage`
classes internally (LoadStage → ParseStage → CleanStage → EnrichStage →
ChunkStage → EmbedStage), so ingestion and indexing share the same stage
code — `ReindexService` does not duplicate parsing/chunking/embedding logic.

Failure handling: on any exception the transaction is rolled back; the new
version is re-added to the session and marked FAILED (committed), so it is
durably recorded while the previously ACTIVE version is left untouched.

**Empirical gotcha (verified with the test DB):** after `session.rollback()`
a flushed-but-uncommitted `IndexVersionDB` is removed from the session
(becomes transient) but keeps its `id` in `__dict__`. `_mark_failed()` must
therefore `session.add(version)` before `fail_version()` + `commit` — calling
`fail_version()` on the rolled-back object alone would never persist the
FAILED row.

- **Testing:** `tests/services/test_reindex_service.py` — success path builds
  v2, activates it, retires v1, and attaches all chunks to v2; failure path
  (embedding provider fails on the third document) marks the new version
  FAILED with zero chunks while v1 stays ACTIVE. The old
  `tests/integration/test_reindex_service.py` (pre-dates this rewrite) was
  deleted.

## 26. Version-aware indexing update — RESOLVED

There was an architectural issue that had to be fixed before relying heavily on simultaneous index versions:

`IndexingService.update()` previously removed **all** chunks for a document.

With multiple index versions, this could remove chunks belonging to an older version.

The correct behavior:

```
Document
   │
   ├── chunks for index v1
   │
   └── chunks for index v2
```

and updating/reindexing one version must not accidentally destroy another version.

This is now **fixed**:

- `IndexingService.update()` resolves the active index version and deletes only that version's chunks (plus their embeddings) for the document, then re-persists into the same version.
- `ChunkRepository.delete_by_document_id(document_id, index_version_id)` scopes the deletion to one version.
- `ChunkRepository.get_by_document_id_and_version(document_id, index_version_id)` gives version-scoped chunk lookup. Note: retrieval's *search* path does **not** currently use version scoping — that is the open defect in §42.
- A uniqueness constraint `uq_chunks_document_version_index` on `(document_id, index_version_id, chunk_index)` prevents duplicate chunk positions inside one version.

Diagram of the invariant:

```
document A / v1 / 0   ✓
document A / v1 / 1   ✓
document A / v2 / 0   ✓
document A / v2 / 1   ✓

document A / v1 / 0   ✗ duplicate (rejected)
```

- **Testing:** `tests/services/test_indexing_service.py` — builds doc A with v1 + v2 chunks, updates in active v2, and asserts v1 keeps its 2 chunks while v2 holds the updated content.

## 27. Ingestion run tracking — FINISHED

Created:

`ingestion_runs`

Pydantic model:

- `IngestionRun`

Fields:

- `id`
- `run_type`
- `status`
- `started_at`
- `completed_at`
- `discovered_count`
- `processed_count`
- `skipped_count`
- `failed_count`
- `error_message`

Repository:

- `IngestionRunRepository`

Service:

- `IngestionRunService`

A pipeline execution now gets:

- `run_id`

## 28. Pipeline run tracking — FINISHED

`IngestionPipeline.run()` now roughly does:

```
start run
    ↓
discover documents
    ↓
record discovered_count
    ↓
process documents
    ↓
track:
    processed
    skipped
    failed
    ↓
complete run
```

Pipeline returns:

- `IngestionResult`

containing:

- `run_id`
- `discovered_count`
- `processed_count`
- `skipped_count`
- `failed_count`
- `document_ids`

## 29. Per-document processing tracking — FINISHED

Created:

`document_processing`

Pydantic model:

- `DocumentProcessingResult`

Fields:

- `id`
- `run_id`
- `document_id`
- `source_uri`
- `operation`
- `status`
- `error_message`

Repository:

- `DocumentProcessingRepository`

Service:

- `DocumentProcessingService`

It records:

- `success`
- `skipped`
- `failed`

Typed by enums in `src/core/enums.py`:

- `IngestionRunStatus` (RUNNING/COMPLETED/FAILED) — run lifecycle
- `DocumentProcessingStatus` (SUCCESS/SKIPPED/FAILED) — record status
- `DocumentProcessingOperation` (ADD/UPDATE/DELETE/SKIP/REINDEX) — operation performed

Commit semantics:

- `record_success()` / `record_skipped()` / `record_failure()` each commit their record immediately, so processing history is durable even if a later document-level transaction rolls back.

Example:

```
run_id: abc
source_uri: data/raw/billing.md
operation: add
status: success
document_id: xyz
```

## 30. Document lifecycle — FINISHED (base; Step 32 will improve it)

We just implemented the foundation for explicit lifecycle states.

Enum:

- `DocumentLifecycleStatus`

Values:

- PENDING
- PROCESSING
- ACTIVE
- FAILED
- DELETED

We intentionally distinguish:

```
Change type
NEW
MODIFIED
UNCHANGED
```

from:

```
Document lifecycle
PENDING
PROCESSING
ACTIVE
FAILED
DELETED
```

These represent different concepts.

## 31. Current desired lifecycle

```
                 Discovery
                     │
                     ▼
             Change Detection
                     │
          ┌──────────┼──────────┐
          │          │          │
         NEW      MODIFIED   UNCHANGED
          │          │          │
          ▼          ▼          └──► SKIP
      PROCESSING  PROCESSING
          │          │
          └────┬─────┘
               ▼
           Processing
               │
        ┌──────┴──────┐
        ▼             ▼
      ACTIVE        FAILED*
```

> * failure history is recorded in `document_processing`; the current database transaction may roll back the document itself to its previous consistent state.

## 32. Tests already created

We have tests covering multiple layers:

```
tests/
├── unit/
│   ├── config
│   ├── core
│   ├── ingestion
│   └── ...
└── integration/
    ├── database
    ├── ingestion
    ├── document lifecycle
    └── ...
```

76 test files, 360 collected tests. Current status: **357 passed, 3 failed**
(the 3 failures are one defect — see §42).

Covered layers:

- document repository / mapping
- filesystem discovery, hashing/change detection
- loading, parsing, cleaning, metadata, chunking, embedding
- database persistence, indexing, index versions, reindexing
- index validation (`tests/services/test_index_validation_service.py`)
- retrieval: vector, keyword, hybrid/RRF, reranking, filters
  (`tests/services/test_retrieval_service.py`,
  `tests/integration/test_vector_search_repository.py`)
- retrieval evaluation: Recall@K/Precision@K/RR/MRR/NDCG
  (`tests/services/test_retrieval_metrics_service.py`)
- ingestion runs, per-document processing, pipeline isolation, finalization
- generation: prompt building, citations, grounding, provider contract
- RAG evaluation: dataset loader, citation/grounding/answer evaluators,
  service + runner (`tests/evaluation/`)
- observability: request context, JSON logging, `Timer`, metrics, registry
  (`tests/observability/`)
- API: health, readiness, `/rag/query`, `/metrics`, error handlers
  (`tests/api/`) — dependency-overridden, never touches the network
- reliability: retry policy, OpenRouter classification/validation,
  exception hierarchy (`tests/providers/`, `tests/security/`)

## 33. Current project architecture

The important implemented portion currently looks like:

149 Python modules under `src/`. Implemented tree:

```
src/
├── core/
│   ├── enums.py, errors.py, hashing.py, ids.py, clock.py, exceptions.py
│
├── models/
│   ├── document.py, chunk.py, embedding.py, indexing.py, ingestion.py
│   ├── index_validation.py, retrieval.py, rag.py, api.py
│
├── config/
│   ├── loader.py, settings.py
│
├── db/
│   ├── base.py, engine.py, session.py
│   ├── models/          document, chunk, embedding, index_version,
│   │                    run, document_processing
│   └── repositories/    documents, chunks, embeddings, index_versions,
│                        vector_search, keyword_search, runs,
│                        document_processing
│
├── services/
│   ├── document_service.py, indexing_service.py, versioning_service.py
│   ├── reindex_service.py, index_validation_service.py
│   ├── retrieval_service.py, ingestion_run_service.py
│   ├── document_processing_service.py
│   ├── generation_service.py, rag_service.py
│   ├── rag_evaluation_service.py, rag_evaluation_runner.py
│   ├── retrieval_metrics_service.py, retrieval_evaluation_runner.py
│   └── ingestion_persistence_service.py   (dead code, see §37)
│
├── ingestion/
│   ├── context.py, pipeline.py, change_detection.py
│   ├── metadata.py, metadata_extractor.py, chunking.py, cleaners/
│   ├── sources/, loaders/, parsers/, chunkers/, stages/
│   │   (discover, load, parse, clean, enrich, chunk, embed, finalizer)
│
├── embeddings/            deprecated re-export shim
│
├── providers/
│   ├── embeddings/        base.py, local.py, factory.py
│   ├── llm/               base.py, openrouter.py, factory.py
│   └── retry.py
│
├── retrieval/
│   ├── pipeline.py        RetrievalPipeline (rerank stage + metrics)
│   ├── search/            base.py (+ reciprocal_rank_fusion),
│   │                      vector.py, keyword.py, hybrid.py
│   └── rerank/            base.py, simple.py
│
├── generation/
│   ├── context_builder.py, prompt_builder.py,
│   ├── citation_extractor.py, grounding.py
│
├── evaluation/
│   ├── rag_dataset_loader.py
│   ├── metrics/           recall_at_k, precision_at_k, reciprocal_rank,
│   │                      mrr, ndcg, aggregate
│   ├── citation/evaluator.py
│   ├── grounding/evaluator.py
│   └── answer/semantic.py  (SimpleAnswerEvaluator + AnswerEvaluator boundary)
│
├── observability/
│   ├── context.py          ContextVar request_id
│   ├── logging.py          JSON formatter + configure_logging
│   ├── metrics.py          thread-safe MetricsCollector
│   ├── registry.py         process-wide singleton
│   └── timer.py            monotonic Timer
│
├── application/
│   └── container.py        ApplicationContainer — the composition root
│
├── api/
│   ├── app.py              create_app(), middleware, routers
│   ├── dependencies.py     get_db_session, get_rag_service
│   ├── errors.py           exception handlers
│   └── routes/             health.py, rag.py, metrics.py
│
└── cli/
    └── evaluate_rag.py     uv run python -m src.cli.evaluate_rag
```

Not yet present (planned): `src/cache/` (performance phase).

Config:

```
config/
├── settings.yaml       application.name, application.environment, logging.level
├── embedding.yaml      provider, model, dimensions
├── llm.yaml            provider, model, temperature, max_tokens
├── ingestion.yaml      filesystem.input_dir / processed_dir / archive_flag
├── reliability.yaml    llm (timeout/retries/delay), retrieval.timeout_seconds,
│                       api.max_query_length / max_top_k
└── profiles/           empty
```

Configuration resolution:

```
config/*.yaml ──► Pydantic models in src/config/settings.py
                        │
.env ───────────────────► EnvironmentSettings (pydantic-settings)
                        │
                        ▼
                    Settings
```

`ingestion.yaml` keeps operational/archive behavior out of Python code, but is
still **not** loaded through the config system — the factory hardcodes
`FileFinalizer(processed_dir=Path("data/processed"), archive_flag=True)`.

## 34. Pipeline per-document isolation — FINISHED

`IngestionPipeline.run()` is now orchestration only; all per-document work moved into `_process_document(run_id, document_input) -> DocumentProcessingResult`:

```
discover documents
        │
        ▼
_process_document (exactly one source document):
        ├── hash → change detection → operation (ADD / UPDATE / SKIP)
        ├── load → parse → clean → enrich → chunk → embed
        ├── index (add/update) via IndexingService
        ├── on success: index + document committed together
        ├── on failure: rollback document transaction, record_failure
        └── finalize source (archive/delete) only after SUCCESS
        │
        ▼
tally processed / skipped / failed from each result → complete or fail run
```

What this guarantees:

- a failed document leaves no partial chunks behind
- one failure does not abort the whole run
- run-level counters reflect exact per-document outcomes
- an `UPDATE` that reaches the persistence layer always has its document present (explicit guard)

Also fixed: `IngestionRunService.start()` now commits the `ingestion_runs` row immediately. Previously a failed document's `IndexingService` rollback could undo the uncommitted run row and break the `document_processing.run_id` foreign key when `record_failure` committed.

- **Testing:** `tests/ingestion/test_pipeline.py` (NEW→ADD→SUCCESS, MODIFIED→UPDATE→SUCCESS, UNCHANGED→SKIP→SKIPPED, exception→FAILED)

## 35. Source finalization (archive/delete) — FINISHED

`FileFinalizer` in `src/ingestion/stages/finalizer.py`.

Behavior mirrors the original `data/raw` → `data/processed` requirement:

```
filesystem:
  input_dir: data/raw
  processed_dir: data/processed
  archive_flag: true
```

- `archive_flag=true` → move the processed source to `processed_dir` (collision-safe: `document.md` → `document_1.md`)
- `archive_flag=false` → delete the source
- missing source → no-op
- finalization runs **only after SUCCESS** — never on FAILED or SKIPPED — so an already-indexed file that reappears in `data/raw` is not archived/deleted by a re-run

Pending: load `processed_dir`/`archive_flag` from `config/ingestion.yaml` through the existing config system instead of the current factory default (`FileFinalizer(processed_dir=Path("data/processed"), archive_flag=True)`).

- **Testing:** `tests/ingestion/stages/test_finalizer.py`; `tests/integration/test_pipeline_finalization.py` (SUCCESS→finalized, FAILED→remains in raw, SKIPPED→remains in raw)

## 36. What remains — implementation roadmap

### Phase A — Finish ingestion/RAGOps foundation

#### Step 31 — FINISHED

Made `document_processing` transaction-safe.

What was fixed:

- `DocumentProcessingService.record_success()`
- `DocumentProcessingService.record_skipped()`
- `DocumentProcessingService.record_failure()`

previously only `flush`-ed; now each method commits its record immediately.

This means processing records survive document-level commits/rollbacks correctly.

- **Testing:** `tests/integration/test_document_processing.py`
  - `test_record_success` no longer commits manually
  - `test_processing_record_is_committed` rolls back the session and confirms the record was durably persisted

#### Step 32 — NEXT

Improve document lifecycle/error handling.

Need to distinguish:

- document state

from:

- processing attempt state

and make failure history durable.

#### Step 33 — FINISHED

Add explicit document operation records with run correlation.

Implemented via `DocumentProcessingOperation`:

- ADD
- UPDATE
- DELETE
- SKIP
- REINDEX

Every `document_processing` record (success/skipped/failure) carries a `run_id` and an `operation`. The pipeline derives the operation from the change type:

```
NEW      → ADD
MODIFIED → UPDATE
UNCHANGED → SKIP
```

- **Testing:** `tests/unit/core/test_ingestion_operations.py`

#### Step 34 — FINISHED

Pipeline per-document isolation (detail in §34).

`IngestionPipeline._process_document(run_id, document_input) -> DocumentProcessingResult` now owns the workflow for exactly one source document:

- change detection (previous hash from persisted document)
- change-type → operation mapping (NEW→ADD, MODIFIED→UPDATE, UNCHANGED→SKIP)
- the load → parse → clean → enrich → chunk → embed stage chain
- success/failure recording (with the explicit `UPDATE`-missing-document guard)

`run()` is orchestration only: discover, iterate `_process_document`, tally `processed`/`skipped`/`failed` from result status, build `document_ids`, then update run counts and complete/fail.

Also fixed: `IngestionRunService.start()` now commits the run immediately — previously a failed document's `IndexingService` rollback could undo the uncommitted `ingestion_runs` row and break the `document_processing` FK when `record_failure` committed.

- **Testing:** `tests/ingestion/test_pipeline.py` (NEW→ADD→SUCCESS, MODIFIED→UPDATE→SUCCESS, UNCHANGED→SKIP→SKIPPED, exception→FAILED)

#### Step 35 — FINISHED

Implement archive/delete behavior (source finalization; detail in §35).

- `config/ingestion.yaml` keeps operational behavior out of Python code:

```
filesystem:
  input_dir: data/raw
  processed_dir: data/processed
  archive_flag: true
```

- `FileFinalizer` in `src/ingestion/stages/finalizer.py`:
  - `archive_flag=true` → move the file to `processed_dir` (collision-safe: `document.md` → `document_1.md`)
  - `archive_flag=false` → delete the file
  - missing source is a no-op
- The pipeline finalizes the source **only after SUCCESS** — never on FAILED or SKIPPED — so an already-indexed file that reappears in `data/raw` is not archived/deleted by a re-run.
- Factory builds `FileFinalizer(processed_dir=Path("data/processed"), archive_flag=True)`.

Pending: load `processed_dir`/`archive_flag` from `config/ingestion.yaml` through the existing config system.

- **Testing:** `tests/ingestion/stages/test_finalizer.py`; `tests/integration/test_pipeline_finalization.py` (SUCCESS→finalized, FAILED→remains in raw, SKIPPED→remains in raw)

### Phase B — Production indexing

#### Step 36 — FINISHED

Fix version-aware indexing.

`IndexingService.update()` is now version-aware: it resolves the active version and deletes/re-persists chunks only for that version, so v1 chunks survive a v2 update.

Supporting changes:

- `ChunkRepository.delete_by_document_id(document_id, index_version_id)` — version-scoped bulk delete
- `ChunkRepository.get_by_document_id_and_version(...)` — version-scoped lookup (useful when retrieval filters by active version)
- `uq_chunks_document_version_index` unique constraint on `(document_id, index_version_id, chunk_index)` in `ChunkDB` (migration `b3f863980aee`)

- **Testing:** `tests/services/test_indexing_service.py`

#### Step 37 — FINISHED

Complete version-aware:

- ADD
- UPDATE
- DELETE
- REINDEX

All four are now version-aware. `IndexRequest.index_version_id` lets an
explicit targeting version override the ACTIVE version; `IndexingService`
resolves it (`_resolve_version`), rejects writes to RETIRED/FAILED versions
(`_validate_writable_version`), and validates each embedding's dimension
against the version (`_validate_embedding_dimensions`). `delete()` removes
only that version's chunks/embeddings for a document and keeps the
`DocumentDB` row. `add()` delegates to `add_to_version`, marks the document
ACTIVE, and commits.

- **Testing:** `tests/services/test_indexing_service.py` — update leaves other
  versions alone, writes to RETIRED/FAILED versions raise, dimension
  mismatches raise; integration delete test renamed accordingly.

#### Step 38 — FINISHED

Complete end-to-end reindex (detail in §25):

```
source
 ↓
discover
 ↓
process (load → parse → clean → enrich → chunk → embed)
 ↓
build new BUILDING index version (add_to_version)
 ↓
validate
 ↓
activate  ──►  retire old ACTIVE version
```

#### Step 39 — FINISHED

Add index validation before activation (detail in §40).

### Phase C — Retrieval — MOSTLY FINISHED (one known defect)

Implemented:

```
query
  ↓
RetrievalService.search()      resolves ACTIVE index version, embeds query,
  ↓                           dimension-checks against that version
RetrievalPipeline.execute()    metrics + timing
  ↓
SearchStrategy.search()
  ├── VectorSearchStrategy     pgvector cosine_distance (src/db/repositories/vector_search.py)
  ├── KeywordSearchStrategy    PostgreSQL FTS: websearch_to_tsquery + ts_rank_cd
  │                           (search_vector TSVECTOR + GIN + trigger)
  └── HybridSearchStrategy     RRF over vector + keyword, candidate_k pool
  ↓
RetrievalFilter                source / document_id / document_type, SQL-side
  ↓
SimpleReranker                 rerank to top_k
```

Models: `RetrievalQuery` (`query`, `top_k` 1–100, optional `candidate_k`
1–500, optional `filters`), `RetrievalFilter`, `RetrievalResult`
(frozen, `extra="forbid"`).

Retrieval metrics implemented in `src/services/retrieval_metrics_service.py`:
Recall@K, Precision@K, RR, MRR, NDCG@K, using stable
`(document_id, chunk_index)` references resolved to chunk IDs against the
ACTIVE version (`src/evaluation/metrics/`).

**Not finished:** active-version SQL scoping (§42), reranking beyond
`SimpleReranker`, and no semantic/learned reranker.

### Phase D — LLM generation — FINISHED (changelog 0.2.9, 0.2.8)

Implemented:

```
src/providers/llm/base.py       LLMProvider contract (transport only)
src/providers/llm/openrouter.py  OpenRouterProvider over httpx
src/providers/llm/factory.py    LLMProviderFactory (key from .env)
src/generation/prompt_builder.py  system prompt + [SOURCE-n] markers,
                                  prompt-injection boundary
src/generation/context_builder.py  provenance formatting (INJECTED BUT UNUSED, §37)
src/generation/citation_extractor.py
src/generation/grounding.py     GroundingService.validate()
src/services/generation_service.py  usage/token tracking, metrics, errors
src/services/rag_service.py     retrieval → generation, returns RAGResponse
```

`config/llm.yaml`: provider, model (`openai/gpt-oss-20b:free`),
temperature, max_tokens. The key stays in `.env` (`OPENROUTER_API_KEY`).

### Phase E — Guardrails — PARTIAL

Implemented: grounding validation (`GroundingService.validate()`) and a
prompt-injection boundary in the system prompt.

**Not implemented:** input rules, output rules, PII detection. Also
`GroundingService.validate()`'s result is **discarded** in
`GenerationService.generate()` — grounding does not yet gate the answer (§37).

### Phase F — Observability — FINISHED (changelog 0.2.12)

Implemented in `src/observability/`:

- `context.py` — `ContextVar` request ID, `X-Request-ID` response header
- `logging.py` — `JsonFormatter` allow-listed fields, `configure_logging()`
- `timer.py` — monotonic `Timer` context manager
- `metrics.py` — thread-safe `MetricsCollector` (counters, durations)
- `registry.py` — process-wide singleton (`get_metrics()`), needed because
  `ApplicationContainer` is built per request
- `GET /metrics`

Metrics emitted: `rag.requests`, `retrieval.requests`,
`retrieval.empty_results`, `generation.requests`, `generation.errors`,
plus latency and token-usage fields in structured logs.

`user_id`, `trace_id`, `retrieval_id` correlation are **not** implemented.

### Phase G — Evaluation — FINISHED (changelog 0.2.3–0.2.6, 0.2.10)

Two independent evaluators exist:

1. **Retrieval metrics** (`src/evaluation/metrics/`, 0.2.6) — Recall@K,
   Precision@K, RR, MRR, NDCG@K against stable chunk references.
2. **RAG evaluation** (0.2.10) — dataset → retrieval → generation → score:

```
data/evaluation/retrieval_v1.yaml   retrieval dataset (18 cases)
data/evaluation/rag_v1.yaml         3 RAG cases (query, expected answer, expected citations)

RAGEvaluationService → CitationEvaluator + GroundingEvaluator + SimpleAnswerEvaluator
RAGEvaluationRunner  → uv run python -m src.cli.evaluate_rag
```

`expected_citations` are positional (`SOURCE-1`), so citation scores depend on
retrieval ranking. `SimpleAnswerEvaluator` is unfiltered reference-token recall,
not semantic correctness. Both shipped datasets are example data, not a
human-reviewed benchmark.

### Phase H — FinOps — PARTIAL

Implemented: token usage and model name are tracked in generation and logged.
**Not implemented:** embedding token counts, cost estimation, cost-per-query /
cost-per-document business metrics.

### Phase I — API — STARTED (changelog 0.2.11–0.2.13)

Implemented in `src/api/`:

```
GET  /health          liveness
GET  /health/ready    database-only readiness
POST /rag/query       RAGQueryRequest → RAGQueryResponse
GET  /metrics
```

- `create_app()` in `app.py`, module-level `app = create_app()`
- `get_db_session` (request-scoped) and `get_rag_service` dependencies
- `X-Request-ID` middleware, sanitized exception handlers with `request_id`
- FastAPI + uvicorn in `pyproject.toml`
- Tests use `app.dependency_overrides` — never the network or a real DB

**Not implemented:** authn/authz, rate limiting, request-size limiting,
CORS configuration, OpenAPI metadata (title/description/version).
Run manually with `uv run uvicorn src.api.app:app`.

### Phase J — CLI — PARTIAL

Only `src/cli/evaluate_rag.py` exists (not a packaged entry point).
Missing: `ingest`, `retrieve`, `index`, `db` subcommands.

### Phase K — Streamlit — NOT STARTED

### Phase L — Testing — PARTIAL

`tests/` has 76 files / 360 tests across `unit/`, `integration/`, `api/`,
`services/`, `evaluation/`, `generation/`, `ingestion/`, `observability/`,
`providers/`, `retrieval/`, `security/`, `models/`, `application/`.

Missing: `golden/` and `fixtures/` directories, E2E tests, regression suites.

### Phase M — CI/CD — NOT STARTED

No `.github/`. Target pipeline: lint → typecheck → unit → integration →
security → build → deploy.

### Phase N — Production hardening — STARTED (changelog 0.2.13)

Implemented: reliability config + bounded models, exception hierarchy,
selective `RetryPolicy`, hardened OpenRouter transport, sanitized API errors,
readiness probe, prompt-injection boundary, `.env.example`, `.gitignore`
secrets rules.

Not implemented: authentication, authorization, rate limiting, database
backups, alerting, runbooks, monitoring/alerting integration.

## 37. Important known technical debt

Keep these in mind when continuing.

1. **Retrieval is not scoped to the ACTIVE index version — OPEN DEFECT**

   `RetrievalService.search()` resolves the ACTIVE version but then **discards
   its id** and delegates to `search_strategy.search(request)`. Neither
   `VectorSearchRepository` nor `KeywordSearchRepository` filters on
   `chunks.index_version_id`, so both return chunks from **every** index
   version. `RetrievalResult.index_version_id` is populated only for
   reporting. This is why 3 tests fail (§42).

   Also note the old repository call signature is gone:
   `search(query_vector, top_k, filters=...)` — there is no `index_version_id`,
   `source`, or `document_id` kwarg anymore (those last two moved into
   `RetrievalFilter`).

2. **Hard-coded embedding dimension**

   `EmbeddingDB.vector` is `Vector(8)` and `config/embedding.yaml` declares
   `dimensions: 8`, matching `LocalEmbeddingProvider`. Both config and column
   are 8-dimensional today, but the column still needs a migration before a
   real provider (OpenAI/Voyage) is used. Also: local config says
   `model: local-dev` while some older fixtures still assume
   `local-deterministic`.

3. **Character chunking is temporary**

   `CharacterTextChunker`, `500` chars, `50` overlap. Needs evaluation
   (`data/evaluation/retrieval_v1.yaml` exists for this) before production.

4. **`ContextBuilder` is injected but never called**

   `GenerationService` takes a `ContextBuilder` and does not use it, so the
   provenance it formats (source URI, chunk index, positions) never reaches
   the LLM prompt. The prompt gets raw chunk text plus `[SOURCE-n]` markers
   built by `PromptBuilder` instead.

5. **Grounding validation result is discarded**

   `GroundingService.validate()` exists and is unit-tested, but
   `GenerationService.generate()` does not use its result. Grounding does not
   gate answers, and `GroundingEvaluator` (evaluation) is a separate concern
   from `GroundingService` (production). No "I don't know" fallback path is
   wired into generation yet.

6. **`reliability.retrieval.timeout_seconds` and `reliability.api.*` are unused**

   Both are parsed and bounded, but nothing reads them: API limits are
   hardcoded in `RAGQueryRequest` (5000 / 20) and retrieval has no timeout.

7. **Non-domain exceptions still leak**

   API error handlers cover the new exception hierarchy, but
   `RetrievalService` and factory/config code still raise raw `ValueError`
   (e.g. `ValueError("No active index version exists")`). `ConfigurationError`
   and `RAGAPIError` handlers exist but those paths are never reached.

8. **`get_next_version_number()` races**

   `MAX(version_number) + 1`. Acceptable for dev; concurrent reindexes would
   collide in production.

9. **`src/services/ingestion_persistence_service.py` is dead code**

   It produces a mypy error (`status` str vs enum, and a missing positional
   `index_version_id` on `ChunkRepository.create`). Superseded by
   `IndexingService`; delete it.

10. **`config/ingestion.yaml` is not loaded**

    `FileFinalizer` is constructed with hardcoded defaults in the container
    rather than from YAML.

11. **`get_next_version_number()` / lifecycle constraints**

    See item 8. `uq_chunks_document_version_index` is in place; stronger
    lifecycle/status CHECK constraints are still future work.

12. **`embeddings.vector` hard-coded `Vector(8)`**

    Same as item 2.

13. **PDF is not implemented**

    The parser registry and source pattern list anticipate PDF, but there is
    no PDF parser or loader. The pipeline factory intentionally uses only
    `("*.md", "*.txt")`.

14. **CI, auth, rate limiting, backups**

    No `.github/` workflows, no authentication/authorization, no rate
    limiting, no backup or alerting story.

## 38. Current RAGOps foundation

At this point we have:

```
                    RAGOps
                      │
          ┌───────────┴───────────┐
          │                       │
   ingestion_runs         document_processing
          │                       │
       run_id                 run_id
       status                 document_id
       counts                 source_uri
       errors                 operation
                               status
                               error
```

This gives us the beginning of operational traceability.

Eventually we want:

```
User Query
    │
request_id
    │
retrieval_id
    │
trace_id
    │
LLM generation
    │
answer
```

and:

```
Ingestion Run
    │
run_id
    │
document processing
    │
document_id
    │
index version
    │
chunks
    │
embeddings
    │
source finalization (archive/delete on SUCCESS)
```

## 39. Current stopping point

The write side is complete and the read side is built end to end: the API
accepts a query, retrieval searches the index, generation calls the LLM with
cited sources, and evaluation can score the result. The project is at
changelog **0.2.13** (Reliability).

**Completed, in changelog order**

- 0.1.24–0.1.39 — index version lifecycle, reindex, validation, version-aware
  writes, ingestion runs, per-document processing, pipeline isolation,
  finalization (§25, §26, §34, §35, §40)
- 0.2.1–0.2.2 — vector retrieval + `RetrievalFilter` (source, document_id,
  document_type) with SQL-side filtering (§41)
- 0.2.3 — keyword retrieval (PostgreSQL FTS: `search_vector` TSVECTOR + GIN +
  trigger, `websearch_to_tsquery` + `ts_rank_cd`)
- 0.2.4 — hybrid retrieval (`reciprocal_rank_fusion`, `HybridSearchStrategy`)
- 0.2.5 — reranking (`Reranker` contract, `SimpleReranker`, `candidate_k`)
- 0.2.6 — retrieval evaluation metrics (Recall@K, Precision@K, RR, MRR, NDCG@K
  over stable `(document_id, chunk_index)` references)
- 0.2.7 — `ApplicationContainer` composition root, `config/embedding.yaml`,
  pytest `importlib` import mode
- 0.2.8 — provider packages under `src/providers/embeddings/`
- 0.2.9 — RAG generation: LLM contract, OpenRouter provider, prompt building,
  citations, grounding, `RAGService`, `config/llm.yaml`
- 0.2.10 — RAG evaluation: dataset loader, citation/grounding/answer
  evaluators, service + runner, `evaluate_rag` CLI
- 0.2.11 — FastAPI app: `/health`, `POST /rag/query`, request-scoped session
- 0.2.12 — observability: request context, JSON logs, `Timer`, metrics
  registry, `/metrics`
- 0.2.13 — reliability: config, exception hierarchy, `RetryPolicy`, hardened
  OpenRouter, sanitized errors, `/health/ready`

**Not started**

- **Performance phase (the immediate next task).** No `src/cache/`,
  no `config/performance.yaml`, no `tests/performance/`, no cache metrics, no
  latency benchmark, no reviewed DB indexes/migration.
- Step 32 — document lifecycle/error handling (outstanding since Phase A).
- FinOps cost accounting, Streamlit, CI/CD, auth, rate limiting.

**Open defect to fix first** — see §42. Retrieval is not scoped to the ACTIVE
index version; this is the cause of all 3 test failures.

The next session should not restart the project. Start from:

```
rag-system
changelog 0.2.13; 357 passed / 3 failed (one defect: active-version scoping)
Next: fix ACTIVE index-version scoping in retrieval
     → then the performance/caching phase (0.2.14)
```

## 40. Index Validation Service — FINISHED

Created this session (changelog 0.1.39).

`src/models/index_validation.py` — `IndexValidationResult`: `valid`,
`document_count`, `chunk_count`, `embedding_count`,
`expected_embedding_dimensions`, `invalid_embedding_count`,
`duplicate_chunk_count`, `documents_without_chunks`,
`chunks_without_embeddings`, and an `errors` list (`extra="forbid"`).

`src/services/index_validation_service.py` — `validate(index_version_id)`:

- raises `ValueError` if the version is missing
- version must be BUILDING (validation runs between build and activation)
- **non-empty guard:** `chunk_count == 0` is invalid — protects against
  activating an empty index after a silent source-discovery failure
- every embedding dimension must equal `version.embedding_dimensions`
- every chunk must have exactly one embedding
- duplicate `(document_id, chunk_index)` positions are counted — this is an
  application-level check; `uq_chunks_document_version_index` already makes
  real duplicates impossible in the DB, so the duplicate detector is
  unit-tested directly rather than through persisted rows

Repository methods added: `ChunkRepository.get_by_index_version_id` and
`EmbeddingRepository.get_by_index_version_id` (embeddings via a `chunks`
join).

`ReindexService` gates activation behind validation: an invalid index is
marked FAILED through the existing rollback path, never activated.

- **Testing:** `tests/services/test_index_validation_service.py` (valid,
  missing embedding, wrong dimensions, empty index, duplicate positions)

## 41. Retrieval — MOSTLY FINISHED (vector + keyword + hybrid + rerank; version scoping open)

Created this session (changelog 0.2.1 and 0.2.2). This is the
"query embedding → vector search → metadata filtering → top-k" segment of
Phase C, later extended by 0.2.3–0.2.5.

**Models** — `src/models/retrieval.py`:

- `RetrievalQuery` — `query`, `top_k` (1–100), optional `candidate_k` (1–500),
  optional `filters`
- `RetrievalFilter` — `source`, `document_id`, `document_type`; frozen,
  `extra="forbid"`
- `RetrievalResult` — chunk/document/version ids, `content`, `chunk_index`,
  `score`, `retrieval_method`; frozen, `extra="forbid"`

**Vector search** — `src/db/repositories/vector_search.py`:
`VectorSearchRepository.search(query_vector, top_k, filters=None)` —
pgvector `cosine_distance` over `embeddings → chunks → documents`, filters
applied SQL-side on `documents`, ordered by distance, limited to `top_k`.

**Keyword search** — `src/db/repositories/keyword_search.py`:
`search(query, top_k, filters=None)` — `websearch_to_tsquery('english', q)`
matched against `chunks.search_vector` with `ts_rank_cd`, same filter handling
(added 0.2.3).

**Strategies** — `src/retrieval/search/`: `VectorSearchStrategy`,
`KeywordSearchStrategy`, `HybridSearchStrategy` (RRF over both, `fusion_k=60`,
`candidate_multiplier=4`), plus `reciprocal_rank_fusion()` in `base.py`.
Strategies embed the query and map rows to `RetrievalResult`.

**Retrieval service** — `src/services/retrieval_service.py`:
`search(request)` resolves the ACTIVE index version (raises `ValueError` if
none), embeds the query via `embedding_provider.embed_query(...)`, raises
`ValueError` on a dimension mismatch against the ACTIVE version, then delegates
to `search_strategy.search(request)`.

⚠ **The resolved `active_version.id` is dropped** and no repository filters on
it — see §42. This is a regression from the original 0.2.1 signature
`search(query_vector, index_version_id, top_k, ...)`.

**Embedding API** — `EmbeddingProvider.embed_query(text)` is a default method
on the base class delegating to `embed([text])`.

**Metadata filtering decision:** document metadata is **not** duplicated onto
chunks; retrieval joins `chunks → documents` and filters on `documents.source` /
`documents.id` / `documents.document_type`. `document_type` **is** now
persisted (`documents.document_type`, migrations `209814ea8e64` /
`236278f35c80`), so the `RetrievalFilter.document_type` filter is live (0.2.2).

**Testing:**

- `tests/services/test_retrieval_service.py` — 2 of 3 pass: `source` filter,
  `document_id` filter, no-active-version → `ValueError`, dimension mismatch →
  `ValueError`. The version-isolation test **fails** (§42).
- `tests/integration/test_vector_search_repository.py` — the two SQL-side
  filter tests **fail** (§42); they still call the removed
  `index_version_id=`/`source=`/`document_id=` kwargs.
- `tests/conftest.py` — shared `embedded_document_factory` fixture.

## 42. Open defect — retrieval is not scoped to the ACTIVE index version

This is the single highest-priority fix and the cause of all 3 test failures.

**What happens**

1. `RetrievalService.search()` resolves the ACTIVE version, uses it only for the
   dimension check, then throws the id away and calls
   `self.search_strategy.search(request)`.
2. `VectorSearchRepository.search()` and `KeywordSearchRepository.search()` have
   no `index_version_id` parameter and no `ChunkDB.index_version_id` predicate.
3. Both return chunks from **every** index version that still holds embeddings.

`RetrievalResult.index_version_id` is populated, but only for reporting — no
caller filters on it.

**Why the tests fail**

- `tests/services/test_retrieval_service.py::test_search_only_returns_chunks_from_active_version`
  — real assertion failure: retired-version chunks come back.
- `tests/integration/test_vector_search_repository.py::test_search_filters_by_source_in_sql`
- `tests/integration/test_vector_search_repository.py::test_search_filters_by_document_id_in_sql`
  — `TypeError: search() got an unexpected keyword argument 'index_version_id'`.
  These two tests were written against the old signature and still pass
  `index_version_id=` / `source=` / `document_id=`.

**Fix direction**

Thread the ACTIVE version id through the search path and add the SQL
predicate — e.g. `RetrievalService` passes `active_version.id` into
`RetrievalQuery` (or a new `index_version_id` argument on
`SearchStrategy.search`), each repository adds
`.where(ChunkDB.index_version_id == index_version_id)`, and the two integration
tests are updated to the `filters=` signature. Watch out for
`HybridSearchStrategy`, which delegates to both sub-strategies and must keep
the version constraint through fusion.

---

**One-line handoff**

> rag-system is a Python 3.12 + uv + Pydantic + SQLAlchemy + Alembic + PostgreSQL/pgvector RAG platform at changelog 0.2.13 (Reliability), with 149 source modules and 76 test files. Write side complete: ingestion → chunking → embedding, version-aware indexing, coordinated `ReindexService` (BUILDING → `IndexValidationService` → activate/retire), index validation, RAGOps run/processing tracking. Read side complete end to end: FastAPI `/health`, `/health/ready`, `POST /rag/query`, `/metrics` → `RetrievalPipeline` → vector/keyword/hybrid(RRF) search + `RetrievalFilter` + `SimpleReranker` → `GenerationService` → OpenRouter LLM with `[SOURCE-n]` prompts and citations. Evaluation (retrieval metrics + RAG citation/grounding/answer) and observability (request context, JSON logs, `Timer`, process-wide metrics registry) are in place; reliability adds bounded config, an exception hierarchy, selective `RetryPolicy`, and sanitized API errors. **Current state: 357 tests pass, 3 fail — all three are one defect (§42): retrieval resolves the ACTIVE index version but discards its id, and neither search repository filters `ChunkDB.index_version_id`, so retired-version chunks leak into results.** Tooling: 75 pre-existing ruff findings, 3 pre-existing mypy errors (`settings.py:115`, `ingestion_persistence_service.py:31/41`), 1 Starlette `httpx2` deprecation warning. `.env` has an empty `OPENROUTER_API_KEY` and the DB is empty (0 documents/chunks/versions), so live `/rag/query` fails at `ValueError: No active index version exists`. Next: fix ACTIVE-version scoping, then the not-yet-started performance/caching phase (`src/cache/`, `config/performance.yaml`, cache metrics, latency benchmark, DB indexes/migration) as changelog 0.2.14.
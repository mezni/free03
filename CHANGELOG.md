# Changelog

All notable changes to `rag-system` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec.php#pec-2.0.0).

## Version History

| Version | Feature Domain | Key Objectives |
|---------|---------------|----------------|
| 0.2.2   | Retrieval Filters | SQL-side `source`/`document_id` filtering via `documents` join in vector search, shared embedded-document test factory |
| 0.2.1   | Retrieval        | `VectorSearchRepository` pgvector cosine search, `RetrievalService` owning query embedding against the active version, `RetrievalQuery`/`RetrievalResult` models |
| 0.1.39  | Index Validation | structured `IndexValidationResult`, `IndexValidationService` guarding activation in `ReindexService`, version-scoped chunk/embedding lookups |
| 0.1.38  | End-to-End Reindex | source→embed coordinated reindex, BUILDING build→validate→ACTIVATE→retire, FAILED on failure keeps previous ACTIVE |
| 0.1.37  | Version-Aware Writes | unified version resolution/validation, explicit-version `add`/`update`/`delete`, single-version delete leaves `DocumentDB` intact |
| 0.1.36  | Version-Aware Chunks | version-scoped chunk delete/lookup, `IndexingService.update()` preserves other versions, `uq_chunks_document_version_index` constraint |
| 0.1.35  | Source Finalization | `FileFinalizer` archive/delete, `config/ingestion.yaml`, finalize-on-SUCCESS gating, durable run start |
| 0.1.34  | Pipeline Isolation | `_process_document` owns the per-document workflow; `run()` orchestrates via `DocumentProcessingResult` counters |
| 0.1.33  | Processing Operations | `DocumentProcessingOperation` enum, change-type→operation mapping in pipeline |
| 0.1.32  | Ingestion Enums   | `IngestionRunStatus`/`DocumentProcessingStatus` enums, enum-typed models & repositories |
| 0.1.31  | Processing Persistence | `DocumentProcessingService` commits per record; rollback-survival persistence test |
| 0.1.30  | Lifecycle Transitions | `DocumentService` set_processing/active/failed, index PROCESSING→ACTIVE flow |
| 0.1.29  | Document Lifecycle | `DocumentLifecycleStatus` enum, enum-typed status, `update_status` |
| 0.1.28  | Document Processing | per-document success/skip/failure records, `DocumentProcessingService` |
| 0.1.27  | Run Tracking | `IngestionResult`, run counter updates, per-document isolation, complete/fail |
| 0.1.26  | Ingestion Runs | `IngestionRun`/`IngestionRunDB`, `ingestion_runs` migration, `IngestionRunService` |
| 0.1.25  | Reindex Service | `add_to_version`, BUILDING/ACTIVE-gated persistence, `ReindexService` build-activate flow |
| 0.1.24  | Version Lifecycle | `IndexVersionStatus` enum, `VersioningService`, create/activate/fail lifecycle |
| 0.1.23  | Version-Aware Indexing | chunk↔version relationships, `IndexVersionRepository` in `IndexingService`, dimension validation |
| 0.1.22  | Index Versions | `IndexVersion`/`IndexVersionDB`, `index_versions` migration, `IndexVersionRepository` |
| 0.1.21  | Indexing | `IndexOperation`, `IndexRequest`, `IndexingService` add/update/delete, reindex flow |
| 0.1.20  | Pipeline | `IngestionPipeline` orchestrating all stages, filesystem factory, E2E tests |
| 0.1.19  | Chunk Persistence | ORM relationships, `ChunkRepository`/`EmbeddingRepository`, `IngestionPersistenceService` |
| 0.1.18  | Vector Storage | pgvector, `ChunkDB`/`EmbeddingDB`, chunks+embeddings migration |
| 0.1.17  | Embeddings | `ChunkEmbedding`/`EmbeddedDocument`, `LocalEmbeddingProvider`, `EmbedStage` |
| 0.1.16  | Chunking | `DocumentChunk`/`ChunkedDocument`, `CharacterTextChunker`, `ChunkStage` |
| 0.1.15  | Metadata | `DocumentMetadata`/`EnrichedDocument`, `FilesystemMetadataExtractor`, `EnrichStage` |
| 0.1.14  | Cleaning | `CleanedDocument`, `TextDocumentCleaner`, `CleanStage` |
| 0.1.13  | Parsing | `ParsedDocument`, Markdown/Text parsers, `ParserRegistry`, `ParseStage` |
| 0.1.12  | Loading | `RawDocument`, `DocumentLoader`, `FilesystemLoader`, `LoadStage` |
| 0.1.11  | Change Detection | SHA-256 hashing, `ChangeDetector`, `DocumentChangeType` |
| 0.1.10  | Ingestion | Document discovery: `DocumentSource`, `FilesystemSource`, `DiscoveryStage` |
| 0.1.9   | Service Layer | `DocumentService` application service, service tests |
| 0.1.8   | Validation    | `DocumentCreate` schema, stricter field constraints, validation tests |
| 0.1.7   | Configuration | Layered YAML + env settings, `load_yaml_config` |
| 0.1.6   | Domain Model | Pydantic `Document` app model, DB→domain conversion |
| 0.1.5   | Repository   | `DocumentRepository` persistence layer, test isolation |
| 0.1.4   | Models & Tests | `DocumentDB` model, integration test suite |
| 0.1.3   | Database      | SQLAlchemy `src/db` module, Alembic migrations |
| 0.1.2   | Infrastructure | Docker Compose, Makefile, .env.example with DATABASE_URL |
| 0.1.1   | Core          | Initial release with config, errors, ids, clock |

## [0.2.3] - 2026-09-25

### Added
- **Reranking:** `Reranker` abstract base class (`src/retrieval/rerank/base.py`) with `rerank()` contract; `SimpleReranker` development implementation (`src/retrieval/rerank/simple.py`) that preserves incoming ranking
- **RetrievalPipeline:** `RetrievalPipeline` now optionally accepts a `Reranker` and applies reranking after retrieval (`src/retrieval/pipeline.py`)
- **`candidate_k` field:** `RetrievalQuery` now carries optional `candidate_k` (`int | None`, 1–500) controlling the candidate pool size before reranking/fusion; when `None`, falls back to `top_k * candidate_multiplier` (`src/models/retrieval.py`)
- **Hybrid search candidate sizing:** `HybridSearchStrategy.search()` uses `request.candidate_k` or falls back to `top_k * candidate_multiplier` for the candidate pool before RRF, returning `candidate_count` results instead of immediately truncating to `top_k` (`src/retrieval/search/hybrid.py`)
- **Testing:** `tests/retrieval/rerank/test_simple.py` — simple reranker order/top_k/validation tests; `tests/retrieval/test_pipeline.py` — pipeline reranking test with `FakeReranker`

### Changed
- `RetrievalService.search()` unchanged — still returns candidates; pipeline layer applies reranking
- `HybridSearchStrategy` candidate counting now respects `candidate_k` before truncation

## [0.2.3] - 2026-09-25

### Added
- **Document type field:** `document_type` column added to `documents` table (String(100), nullable)
- **Pydantic models:** `document_type` field added to both `DocumentCreate` and `Document` models with `max_length=100`
- **Retrieval filtering:** `RetrievalQuery` now carries optional `document_type` filter (min 1 / max 100 chars)
- **Vector search:** `VectorSearchRepository.search()` applies `document_type` filter in SQL via `DocumentDB.document_type`
- **Indexing pipeline:** `document_type` passed from `EnrichedDocument.metadata.document_type` through `DocumentCreate` → `DocumentDB` → persistence
- **Repository methods:** `DocumentRepository.create()` and `update_content_hash()` now persist `document_type`; `to_domain()` converts it to application model
- **RetrievalService:** forwards `request.document_type` to the repository for SQL-side filtering

### Changed
- `RetrievalService.search()` now forwards `request.document_type` to the repository
- `document_type` no longer deferred — fully wired from metadata extraction through persistence to retrieval filtering
- `DocumentRepository.update_content_hash()` now also updates `document_type` (clears if metadata says `None`)

### Fixed
- Metadata refresh limitation: when newly extracted metadata has `document_type=None`, the previous value is now cleared (previously only `title` behavior was non-preserving)

## [0.2.4] - 2026-09-25

### Added
- **RetrievalFilter model:** New `RetrievalFilter` class in `src/models/retrieval.py` consolidating `source`, `document_id`, and `document_type` filters into a single reusable object
- **Unified filter API:** `RetrievalQuery.filters` field replaces individual filter arguments in `search()` calls

### Changed
- `RetrievalQuery` now uses `filters: RetrievalFilter | None` instead of individual `source`, `document_id`, `document_type` fields
- `VectorSearchRepository.search()` accepts `filters: RetrievalFilter | None` and applies all filters from the object
- `RetrievalService.search()` forwards `request.filters` to the repository instead of individual filter fields
- All existing filter tests updated to use `RetrievalFilter(source="...", document_id=..., document_type=...)`

### Fixed
- Test cleanup: removed duplicate filter field parameters from `RetrievalQuery` construction in test files
- Consistent filter validation: all filter fields now go through the `RetrievalFilter` Pydantic model with `extra="forbid"`

## [0.2.4] - 2026-09-25

### Added
- **RetrievalFilter model:** New `RetrievalFilter` class in `src/models/retrieval.py` consolidating `source`, `document_id`, and `document_type` filters into a single reusable object
- **Unified filter API:** `RetrievalQuery.filters` field replaces individual filter arguments in `search()` calls

### Changed
- `RetrievalQuery` now uses `filters: RetrievalFilter | None` instead of individual `source`, `document_id`, `document_type` fields
- `VectorSearchRepository.search()` accepts `filters: RetrievalFilter | None` and applies all filters from the object
- `RetrievalService.search()` forwards `request.filters` to the repository instead of individual filter fields
- All existing filter tests updated to use `RetrievalFilter(source="...", document_id=..., document_type=...)`

### Fixed
- Test cleanup: removed duplicate filter field parameters from `RetrievalQuery` construction in test files
- Consistent filter validation: all filter fields now go through the `RetrievalFilter` Pydantic model with `extra="forbid"`

## [0.2.5] - 2026-09-25

### Added
- **PostgreSQL full-text search:** `search_vector` column (TSVECTOR) added to `chunks` table with GIN index
- **Full-text search trigger:** Automatic `search_vector` population on chunk insert/update via PostgreSQL trigger function
- **KeywordSearchRepository:** `KeywordSearchRepository.search()` enables `websearch_to_tsquery`/`ts_rank_cd` queries against `search_vector`
- **KeywordSearchStrategy:** New `SearchStrategy` implementation for PostgreSQL full-text search
- **Retrieval pipeline diversification:** `RetrievalService` now accepts any `SearchStrategy` (vector or keyword), decoupling search logic from the service layer

### Changed
- `SearchStrategy` base class updated to accept `RetrievalQuery` instead of separate queryVector/top_k/filters parameters
- `VectorSearchStrategy.search()` now takes `RetrievalQuery` and delegates embedding to `EmbeddingProvider`
- `KeywordSearchStrategy.search()` now takes `RetrievalQuery` and delegates query processing to `KeywordSearchRepository`
- `RetrievalService` constructor now accepts `search_strategy` instead of `vector_search_repository` + `embedding_provider`
- `ChunkDB` model now includes `search_vector: Mapped[str | None] = mapped_column(TSVECTOR, nullable=True)`

### Fixed
- Metadata consistency: `search_vector` is now automatically maintained via PostgreSQL trigger, ensuring tsvector is always in sync with `content`
- Test cleanup: retrieval service tests updated to use new `RetrievalService(index_version_repository, search_strategy)` constructor signature

### Fixed
- Metadata consistency: `search_vector` is now automatically maintained via PostgreSQL trigger, ensuring tsvector is always in sync with `content`
- Test cleanup: retrieval service tests updated to use new `RetrievalService(index_version_repository, search_strategy)` constructor signature

## [0.2.5] - 2026-09-25

### Added
- **PostgreSQL full-text search:** `search_vector` column (TSVECTOR) added to `chunks` table with GIN index
- **Full-text search trigger:** Automatic `search_vector` population on chunk insert/update via PostgreSQL trigger function
- **KeywordSearchRepository:** `KeywordSearchRepository.search()` enables `websearch_to_tsquery`/`ts_rank_cd` queries against `search_vector`
- **KeywordSearchStrategy:** New `SearchStrategy` implementation for PostgreSQL full-text search
- **Retrieval pipeline diversification:** `RetrievalService` now accepts any `SearchStrategy` (vector or keyword), decoupling search logic from the service layer

### Changed
- `SearchStrategy` base class updated to accept `RetrievalQuery` instead of separate queryVector/top_k/filters parameters
- `VectorSearchStrategy.search()` now takes `RetrievalQuery` and delegates embedding to `EmbeddingProvider`
- `KeywordSearchStrategy.search()` now takes `RetrievalQuery` and delegates query processing to `KeywordSearchRepository`
- `RetrievalService` constructor now accepts `search_strategy` instead of `vector_search_repository` + `embedding_provider`
- `ChunkDB` model now includes `search_vector: Mapped[str | None] = mapped_column(TSVECTOR, nullable=True)`

### Fixed
- Metadata consistency: `search_vector` is now automatically maintained via PostgreSQL trigger, ensuring tsvector is always in sync with `content`
- Test cleanup: retrieval service tests updated to use new `RetrievalService(index_version_repository, search_strategy)` constructor signature

## [0.2.6] - 2026-09-25

### Added
- **Reciprocal Rank Fusion helper:** `reciprocal_rank_fusion()` function in `src/retrieval/search/base.py` for combining multiple ranked result lists
- **HybridSearchStrategy:** New `SearchStrategy` implementation that fuses vector and keyword search results using RRF
- **Diversified retrieval:** `HybridSearchStrategy` supports `fusion_k` and `candidate_multiplier` parameters for controlling search scope and fusion behavior

### Changed
- `reciprocal_rank_fusion()` is a reusable utility function that can be used independently or by `HybridSearchStrategy`
- `HybridSearchStrategy.search()` first expands results by `candidate_multiplier` before fusion to ensure sufficient candidates are considered before returning the top `top_k` results

### Fixed
- Metadata consistency: `search_vector` is now automatically maintained via PostgreSQL trigger, ensuring tsvector is always in sync with `content`
- Test cleanup: retrieval service tests updated to use new `RetrievalService(index_version_repository, search_strategy)` constructor signature

## [0.2.5] - 2026-09-25

### Added
- **PostgreSQL full-text search:** `search_vector` column (TSVECTOR) added to `chunks` table with GIN index
- **Full-text search trigger:** Automatic `search_vector` population on chunk insert/update via PostgreSQL trigger function
- **KeywordSearchRepository:** `KeywordSearchRepository.search()` enables `websearch_to_tsquery`/`ts_rank_cd` queries against `search_vector`
- **KeywordSearchStrategy:** New `SearchStrategy` implementation for PostgreSQL full-text search
- **Retrieval pipeline diversification:** `RetrievalService` now accepts any `SearchStrategy` (vector or keyword), decoupling search logic from the service layer

### Changed
- `SearchStrategy` base class updated to accept `RetrievalQuery` instead of separate queryVector/top_k/filters parameters
- `VectorSearchStrategy.search()` now takes `RetrievalQuery` and delegates embedding to `EmbeddingProvider`
- `KeywordSearchStrategy.search()` now takes `RetrievalQuery` and delegates query processing to `KeywordSearchRepository`
- `RetrievalService` constructor now accepts `search_strategy` instead of `vector_search_repository` + `embedding_provider`
- `ChunkDB` model now includes `search_vector: Mapped[str | None] = mapped_column(TSVECTOR, nullable=True)`

### Fixed
- Metadata consistency: `search_vector` is now automatically maintained via PostgreSQL trigger, ensuring tsvector is always in sync with `content`
- Test cleanup: retrieval service tests updated to use new `RetrievalService(index_version_repository, search_strategy)` constructor signature

## [0.2.6] - 2026-09-25

### Added
- **Reciprocal Rank Fusion helper:** `reciprocal_rank_fusion()` function in `src/retrieval/search/base.py` for combining multiple ranked result lists
- **HybridSearchStrategy:** New `SearchStrategy` implementation that fuses vector and keyword search results using RRF
- **Diversified retrieval:** `HybridSearchStrategy` supports `fusion_k` and `candidate_multiplier` parameters for controlling search scope and fusion behavior

### Changed
- `reciprocal_rank_fusion()` is a reusable utility function that can be used independently or by `HybridSearchStrategy`
- `HybridSearchStrategy.search()` first expands results by `candidate_multiplier` before fusion to ensure sufficient candidates are considered before returning the top `top_k` results

## [0.2.1] - 2026-09-23

The system can now query its built index: a search goes through a new retrieval
layer that embeds the query, finds the nearest chunks in the **active** index
version, and returns ranked results.

### Added
- **Retrieval models:** `RetrievalQuery` (`query` min length 1, `top_k` 1–100) and `RetrievalResult` (chunk/document/version IDs, chunk content + index, cosine-distance `score`) in `src/models/retrieval.py`, both frozen with `extra="forbid"`
- **Vector search repository:** `VectorSearchRepository.search()` in `src/db/repositories/vector_search.py` — pgvector `cosine_distance` query over a single index version (join `embeddings` → `chunks`, ordered by distance, limited to `top_k`)
- **Retrieval service:** `RetrievalService` in `src/services/retrieval_service.py` — resolves the ACTIVE index version (raises `ValueError` if none exists), embeds the query via the injected `embedding_provider`, verifies the query embedding dimension matches the active version (else `ValueError`), and returns the top-`k` `RetrievalResult`s
- **Embedding API:** `EmbeddingProvider.embed_query(text)` default on the base class, delegating to `embed([text])`, so every provider can embed a single query without new implementations
- **Testing:** `tests/services/test_retrieval_service.py` (pgvector integration against Docker Postgres) — version isolation (v1 RETIRED chunks never returned while v2 ACTIVE is searched), no-active-version → `ValueError`, query-dimension mismatch → `ValueError`

### Changed
- **Semantic bump:** 0.1.x patch track → 0.2.x minor track, reflecting the system evolving from index-*writing* only into a writable *and searchable* index

## [0.1.39] - 2026-09-23

### Added
- **Validation model:** `IndexValidationResult` (in `src/models/index_validation.py`) — structured validation output with `valid` flag plus `document_count`/`chunk_count`/`embedding_count`, `expected_embedding_dimensions`, `invalid_embedding_count`, `duplicate_chunk_count`, `documents_without_chunks`, `chunks_without_embeddings`, and an `errors` list; `extra="forbid"` config
- **IndexValidationService:** `IndexValidationService` (in `src/services/index_validation_service.py`) with `validate(index_version_id)` returning `IndexValidationResult` and raising `ValueError` for unknown versions. Checks: version must be BUILDING, at least one chunk present (protects against replacing a working index with an empty one after silent source-discovery failure), every embedding dimension must match the version, every chunk must have exactly one embedding, and no duplicate `(document_id, chunk_index)` positions
- **Repository method:** `ChunkRepository.get_by_index_version_id` — version-scoped chunk lookup ordered by `(document_id, chunk_index)`
- **Repository method:** `EmbeddingRepository.get_by_index_version_id` — version-scoped embeddings via a `chunks` join
- **Testing:** `tests/services/test_index_validation_service.py` — valid index, missing embedding (delete one embedding), wrong dimensions (declared 1536 on an 8-dim version), empty index, and duplicate-position detection (unit-tested at the application level, since `uq_chunks_document_version_index` prevents real duplicates in the DB)

### Changed
- **Reindex:** `ReindexService` now takes a `validation_service` dependency and runs `validation_service.validate()` between build and activate — a reindex only reaches `ACTIVE` when the built version is structurally sound; invalid versions are marked `FAILED` via the existing rollback path
- **Reindex:** the internal `_validate_version` BUILDING-only guard is superseded by the full validation service

## [0.1.38] - 2026-09-23

### Added
- **Reindex:** `ReindexService` now coordinates the existing ingestion components end-to-end — injected `VersioningService`, `IndexingService`, and source/loader/parser registry/cleaner/metadata extractor/chunker/embedding provider — instead of accepting pre-embedded documents. Internally it builds the existing `PipelineStage`s, so `_build_version(version_id)` runs `load → parse → clean → enrich → chunk → embed` and persists each document into the target BUILDING version via `add_to_version`
- **Reindex:** `_validate_version(version_id)` — post-build guard raising `ValueError` if the version is missing or no longer `BUILDING`
- **Versioning:** `VersioningService.get_version(version_id) -> IndexVersion | None` with a `to_domain` mapper (`IndexVersionDB` → Pydantic `IndexVersion`); `reindex()` returns the domain model
- **Testing:** `tests/services/test_reindex_service.py` — success path (reindex builds v2, activates it, retires v1, all chunks attached to v2) and failure path (embedding failure on the third document marks the new version FAILED with zero chunks while v1 stays ACTIVE, so the system never loses its active index)

### Changed
- **Reindex:** `reindex(embedding_model, embedding_dimensions) -> IndexVersion` replaces the old explicitly-passed `documents` parameter; it now discovers and processes the source itself
- **Reindex:** failure handling rolls back, re-persists the failed version as `FAILED` (re-added to the session so it survives an inner `add_to_version` rollback), commits, and re-raises — the previously ACTIVE version is left untouched
- **Removed:** obsolete `ReindexService.create_reindex_version`/`index_document`/`activate`/`fail` helpers (replaced by the coordinated `reindex()` flow); `tests/integration/test_reindex_service.py` deleted in favor of the new service-level suite

### Tooling
- **Dev dependency:** `mypy` added to the dev dependency group so `uv run mypy src` works

## [0.1.37] - 2026-09-23

### Added
- **Model:** `IndexRequest.index_version_id: UUID | None` — explicit index-version targeting alongside `document_id`
- **Indexing:** `IndexingService._resolve_version(index_version_id)` — single version-selection point: explicit version (not-found raises `ValueError`) or the active version (none raises `ValueError`)
- **Indexing:** `IndexingService._validate_writable_version(version)` — rejects writes to `RETIRED`/`FAILED` versions (`BUILDING`/`ACTIVE` only)
- **Indexing:** `IndexingService._validate_embedding_dimensions(data, version)` — rejects embeddings whose dimensions differ from the version's `embedding_dimensions` before persistence
- **Testing:** `tests/services/test_indexing_service.py` version-isolation cases — ADD targets the active version by default; UPDATE in a BUILDING v2 while v1 is ACTIVE leaves v1 chunks untouched and replaces v2's; DELETE from v2 leaves v1 chunks and the `DocumentDB` row intact; writes to RETIRED/FAILED versions raise `ValueError`; dimension-mismatched embeddings raise `ValueError`

### Changed
- **Indexing:** `add()`, `update()`, `delete()` now accept an optional `index_version_id` and resolve it through `_resolve_version`, defaulting to the active version
- **Indexing:** `add()` delegates persistence to `add_to_version` (single code path), then marks the document `ACTIVE` and commits
- **Indexing:** `delete(document_id, index_version_id)` no longer removes the `DocumentDB` row — it removes only that version's chunks (embeddings cascade), keeping the document record; removing a document from the index across versions is now an explicit per-version operation
- **Indexing:** `_persist_chunks_and_embeddings` takes the resolved `IndexVersionDB` (not a raw id) and relies on the public write paths for version/dimension validation
- **Reindex:** `ReindexService` continues to call `add_to_version` with an explicit BUILDING version, never accidentally resolving the active version

### Testing
- **Test updated:** `tests/integration/test_ingestion_pipeline.py::test_indexing_service_removes_document_from_active_index` (renamed from `test_indexing_service_deletes_document`) — asserts chunks are gone after `delete()` while the `DocumentDB` row remains

## [0.1.36] - 2026-09-20

### Added
- **Repository:** `ChunkRepository.get_by_document_id_and_version(document_id, index_version_id)` — version-scoped chunk lookup (usable by retrieval filtered on the active version)
- **DB constraint:** `uq_chunks_document_version_index` — `unique(document_id, index_version_id, chunk_index)` on `chunks` (`ChunkDB.__table_args__`), migrated via `b3f863980aee`

### Changed
- **Repository:** `ChunkRepository.delete_by_document_id` now takes `index_version_id` and bulk-deletes (`synchronize_session=False`) only chunks belonging to that version
- **Indexing:** `IndexingService.update()` resolves the active index version and deletes/re-persists chunks only for it, so updating one version never destroys another version's chunks (their embeddings are removed first via `delete_by_chunk_ids`)

### Testing
- **Testing:** `tests/services/test_indexing_service.py` — doc A indexed into v1 and v2, then updated in the active v2; asserts v1 keeps its original two chunks while v2 holds the re-indexed content

## [0.1.35] - 2026-09-20

### Added
- **Config:** `config/ingestion.yaml` with `filesystem.input_dir`/`processed_dir`/`archive_flag` (operational behavior out of Python code; YAML loading to come)
- **Finalizer:** `FileFinalizer` in `src/ingestion/stages/finalizer.py` — archive mode (`shutil.move` with `_unique_destination` collision handling: `document.md` → `document_1.md`) or delete mode (`unlink`); missing-source noop
- **Testing:** `tests/ingestion/stages/test_finalizer.py` (archive, delete, collision, noop); `tests/integration/test_pipeline_finalization.py` (SUCCESS→finalized, FAILED→source stays in raw, SKIPPED→source stays in raw)

### Changed
- **Pipeline:** `IngestionPipeline` now requires `finalizer: FileFinalizer`; `run()` finalizes the source file only after `SUCCESS` — never on `FAILED` or `SKIPPED`, so an already-indexed file reappearing in `data/raw` is not archived/deleted by a re-run
- **Factory:** `create_filesystem_ingestion_pipeline` builds `FileFinalizer(processed_dir=Path("data/processed"), archive_flag=True)` (overridable) and passes it to the pipeline

### Fixed
- **Run durability:** `IngestionRunService.start()` now commits the run immediately; previously a failed document's `IndexingService` rollback could undo the uncommitted `ingestion_runs` row, breaking the `document_processing` FK when `record_failure` committed

### Testing
- **Tests updated:** `tests/integration/test_ingestion_pipeline.py` restructured to sibling `raw/`/`processed/` dirs (recursive discovery was re-indexing archived copies); skip test now verifies restore-and-skip leaves the source in place

## [0.1.34] - 2026-09-20

### Changed
- **Pipeline:** per-document work extracted into `IngestionPipeline._process_document(run_id, document_input) -> DocumentProcessingResult`, which owns change detection, change-type→operation mapping, the load→parse→clean→enrich→chunk→embed stage chain, and success/failure recording (including the explicit `UPDATE`-missing-document guard)
- **Pipeline:** `run()` is now orchestration only — discover, call `_process_document` per input, tally `processed`/`skipped`/`failed` from result status, build `document_ids` from successful results, then update run counts and complete/fail
- **Pipeline:** internal `_operation_for` maps `DocumentChangeType`→`DocumentProcessingOperation`; `_to_result` converts persisted records to `DocumentProcessingResult`

### Testing
- **Testing:** `tests/ingestion/test_pipeline.py` — NEW→ADD→SUCCESS, MODIFIED→UPDATE→SUCCESS, UNCHANGED→SKIP→SKIPPED, and processing-exception→FAILED with `error_message`, exercised without a database via fake session/repositories

## [0.1.33] - 2026-09-19

### Added
- **Enum:** `DocumentProcessingOperation` (ADD/UPDATE/DELETE/SKIP/REINDEX) in `src/core/enums.py`
- **Models:** `DocumentProcessingResult.operation` typed `DocumentProcessingOperation`

### Changed
- **Service:** `DocumentProcessingService` `record_success`/`record_skipped`/`record_failure` now accept `DocumentProcessingOperation` (the recorded `operation` column uses `.value`); `record_skipped` no longer takes an `operation` argument and always writes `SKIP`
- **Pipeline:** maps change type to operation (NEW→ADD, MODIFIED→UPDATE, UNCHANGED→SKIP) and records that operation for success/failure attempts

### Testing
- **Testing:** `tests/unit/core/test_ingestion_operations.py`; integration test passes `DocumentProcessingOperation.ADD` and asserts `record.operation == "add"`

## [0.1.32] - 2026-09-19

### Added
- **Enums:** `IngestionRunStatus` (RUNNING/COMPLETED/FAILED) and `DocumentProcessingStatus` (SUCCESS/SKIPPED/FAILED) in `src/core/enums.py`
- **Models:** `IngestionRun.status` typed `IngestionRunStatus` (default RUNNING); `DocumentProcessingResult.status` typed `DocumentProcessingStatus`
- **Repository:** `IngestionRunRepository` writes `IngestionRunStatus.*.value` for create/complete/fail
- **Service:** `DocumentProcessingService` writes `DocumentProcessingStatus.*.value` for success/skipped/failed
- **Testing:** `tests/unit/core/test_ingestion_enums.py`

## [0.1.31] - 2026-09-19

### Changed
- **Service:** `DocumentProcessingService` `record_success`/`record_skipped`/`record_failure` now commit the session per record, so processing records persist independently of later run commits

### Testing
- **Testing:** `test_record_success` no longer calls `database_session.commit()`; adds `test_processing_record_is_committed` verifying records survive a `database_session.rollback()`

## [0.1.30] - 2026-09-16

### Added
- **Service:** `DocumentService.set_processing`, `set_active`, `set_failed` lifecycle transitions
- **Indexing:** new documents start `PROCESSING` (`_build_document_data`) and move to `ACTIVE` after chunks/embeddings persist; `update()` transitions PROCESSING→ACTIVE, with rollback leaving the previous ACTIVE state intact on failure
- **Testing:** `tests/integration/test_document_lifecycle.py`

## [0.1.29] - 2026-09-16

### Added
- **Enums:** `DocumentLifecycleStatus` (PENDING/PROCESSING/ACTIVE/FAILED/DELETED)
- **Models:** `DocumentCreate`/`Document` status now typed `DocumentLifecycleStatus` (default PENDING)
- **Repository:** `DocumentRepository.update_status`
- **Indexing:** `IndexingService._build_document_data` marks new documents `ACTIVE`
- **Testing:** `tests/unit/core/test_document_lifecycle.py`; document tests updated to enum statuses; index-version tests use `IndexVersionStatus`

## [0.1.28] - 2026-09-16

### Added
- **Model:** `DocumentProcessingResult` in `src/models/ingestion.py`
- **DB model:** `DocumentProcessingDB` (`document_processing`, FKs to runs/documents) migrated via `f6479a21dd17`
- **Repository:** `DocumentProcessingRepository` (`create`, `get_by_run_id`)
- **Service:** `DocumentProcessingService` (`record_success`, `record_skipped`, `record_failure`)
- **Pipeline:** unmatched/success/failure events recorded per document; pipeline tests still pass
- **Testing:** `tests/integration/test_document_processing.py`

## [0.1.27] - 2026-09-16

### Added
- **Model:** `IngestionResult` (`run_id`, counts, `document_ids`) in `src/ingestion/context.py`
- **Repository:** `IngestionRunRepository.update_counts`
- **Service:** `IngestionRunService.update_counts`
- **Pipeline:** `run()` now starts an ingestion run, isolates per-document failures (increments `failed_count`, continues), aggregates counters into the run, then completes; pipeline-level failures mark the run failed and re-raise
- **Testing:** pipeline integration tests updated to assert on `IngestionResult`

## [0.1.26] - 2026-09-16

### Added
- **Model:** `IngestionRun` Pydantic model (`src/models/ingestion.py`)
- **DB model:** `IngestionRunDB` (`ingestion_runs` table) migrated via `e8c4e4f33447`
- **Repository:** `IngestionRunRepository` (`create`, `get_by_id`, `mark_completed`, `mark_failed`)
- **Service:** `IngestionRunService` (`start`, `complete`, `fail`)
- **Testing:** `tests/integration/test_ingestion_runs.py`; conftest teardown clears `ingestion_runs`

## [0.1.25] - 2026-09-16

### Added
- **Service:** `ReindexService` — build a new index version, index documents into it, then activate; rollback on failure without touching version state
- **Indexing:** `IndexingService.add_to_version` adds a document to a specific BUILDING version; `_persist_chunks_and_embeddings` now takes an explicit `index_version_id` and validates the version exists and is BUILDING/ACTIVE
- **Repository:** `IndexVersionRepository.get_by_id`
- **Testing:** `tests/integration/test_reindex_service.py`
- `add()`/`update()` now resolve the active index version and pass it to persistence

## [0.1.24] - 2026-09-16

### Added
- **Enums:** `IndexVersionStatus` (`BUILDING`, `ACTIVE`, `RETIRED`, `FAILED`) in `src/core/enums.py`
- **Repository:** `IndexVersionRepository` lifecycle — `get_next_version_number`, `create_building`, `activate` (retires prior active versions), `mark_failed`
- **Service:** `VersioningService` (`create_version`, `activate_version`, `fail_version`, `get_active_version`)
- **Model:** `IndexVersion` status now typed as `IndexVersionStatus` in `src/models/indexing.py`
- **Testing:** `tests/integration/test_versioning_service.py`; integration teardown now cleans `index_versions` for deterministic isolation

## [0.1.23] - 2026-09-16

### Added
- **ORM relationships:** `ChunkDB.index_version` ↔ `IndexVersionDB.chunks` via `back_populates`
- **Repository:** `ChunkRepository.create` now accepts and persists `index_version_id`
- **Service:** `IndexingService` wires `IndexVersionRepository`, resolves the active version via `_get_active_index_version` (raises `RuntimeError` if none active), and validates each embedding's dimensions against the active version before persisting
- **Testing:** `tests/integration/test_index_versioning.py`; integration `conftest.py` seeds an active version (v1, `local-deterministic`, 8 dims); previously skipped pipeline tests now run and pass

## [0.1.22] - 2026-09-16

### Added
- **Model:** `IndexVersion` in `src/models/indexing.py` — version metadata (status, embedding model/dimensions, activation timestamps)
- **Database model:** `IndexVersionDB` in `src/db/models/index_version.py` (`index_versions` table with `activated_at`)
- **Schema:** `ChunkDB.index_version_id` — NOT NULL FK to `index_versions` (`ondelete=RESTRICT`); migration `e71285cbb8e1` also establishes the `index_versions → chunks → embeddings` versioning chain
- **Repository:** `IndexVersionRepository` in `src/db/repositories/index_versions.py` (`create`, `get_active`, `get_by_version_number`) exported from `src/db/repositories/__init__.py`
- **Note:** pipeline integration tests marked skipped pending `IndexingService` awareness of the active index version (per design)

## [0.1.21] - 2026-09-16

### Added
- **Enum:** `IndexOperation` (`ADD`, `UPDATE`, `DELETE`, `REINDEX`) in `src/core/enums.py`
- **Model:** `IndexRequest` in `src/models/indexing.py` — operation, optional `document_id`, optional reason
- **Repositories:** `EmbeddingRepository.delete_by_chunk_ids`, `DocumentRepository.update_content_hash`
- **Service:** `IndexingService` in `src/services/indexing_service.py` — `add`, `update` (replaces chunks/embeddings), `delete` (cascades), transactional with rollback
- **Pipeline:** `IngestionPipeline` now uses `IndexingService`; modified documents are reindexed via `update` instead of raising `NotImplementedError`
- **Testing:** `test_modified_document_is_reindexed`, `test_indexing_service_deletes_document`

## [0.1.20] - 2026-09-16

### Added
- **Pipeline:** `IngestionPipeline` in `src/ingestion/pipeline.py` rewritten on the `PipelineStage` API — chains discover → load → parse → clean → enrich → chunk → embed stages, skips unchanged documents via `DocumentChangeType`, raises `NotImplementedError` for modified documents (reserving indexing/versioning), and persists via `IngestionPersistenceService`
- **Factory:** `create_filesystem_ingestion_pipeline` in `src/ingestion/factory.py` wiring a filesystem-based source/loader, Markdown+Text `ParserRegistry`, text cleaner, metadata extractor, character chunker, and local embedding provider
- **Testing:** `tests/integration/test_ingestion_pipeline.py` with end-to-end pipeline test and unchanged-document skip test

## [0.1.19] - 2026-09-16

### Added
- **ORM relationships:** `DocumentDB.chunks` (cascade `all, delete-orphan`) and `ChunkDB.document` via `back_populates` with `TYPE_CHECKING` imports
- **Repositories:** `ChunkRepository` in `src/db/repositories/chunks.py` (`create`, `get_by_document_id`, `delete_by_document_id`) and `EmbeddingRepository` in `src/db/repositories/embeddings.py` (`create`, `get_by_chunk_id`)
- **Service:** `IngestionPersistenceService` in `src/services/ingestion_persistence_service.py` persisting an `EmbeddedDocument`, its chunks, and embeddings in one transaction with rollback on failure
- **Context:** `ChunkedDocument` and `EmbeddedDocument` now carry `metadata: DocumentMetadata`; `ChunkStage` and `EmbedStage` thread it through
- **Testing:** `tests/integration/test_ingestion_persistence.py`

## [0.1.18] - 2026-09-16

### Added
- **Infrastructure:** Docker Compose postgres service switched to `pgvector/pgvector:pg17`; `pgvector` added as Python dependency
- **Database models:** `ChunkDB` in `src/db/models/chunk.py` (chunks table with `document_id` FK cascade) and `EmbeddingDB` in `src/db/models/embedding.py` (embeddings table with pgvector `Vector(8)` column, unique `chunk_id` FK cascade)
- **Registration:** `src/db/models/__init__.py` and `src/db/base.py` now expose `ChunkDB` and `EmbeddingDB`
- **Migration:** `1f3f84629772` — enables the `vector` extension, creates `chunks` and `embeddings` tables with indexes

## [0.1.17] - 2026-09-16

### Added
- **Ingestion context:** `ChunkEmbedding` and `EmbeddedDocument` in `src/ingestion/context.py` — models for per-chunk vectors and embedded documents
- **Embeddings:** `EmbeddingProvider` base interface in `src/embeddings/base.py`; `LocalEmbeddingProvider` in `src/embeddings/local.py` producing normalized, deterministic SHA-256-derived vectors for development and tests
- **Exports:** `src/embeddings/__init__.py` re-exports `EmbeddingProvider` and `LocalEmbeddingProvider`
- **Stage:** `EmbedStage[ChunkedDocument, EmbeddedDocument]` in `src/ingestion/stages/embed.py`
- **Testing:** `tests/unit/embeddings/test_local.py`, `tests/unit/ingestion/test_embed_stage.py`

## [0.1.16] - 2026-09-16

### Added
- **Ingestion context:** `DocumentChunk` and `ChunkedDocument` in `src/ingestion/context.py` — models for character-range chunks of an enriched document
- **Chunking:** `DocumentChunker` base interface in `src/ingestion/chunking.py`; `CharacterTextChunker` in `src/ingestion/chunkers/text.py` splitting content into fixed-size overlapping chunks with configuration validation
- **Exports:** `src/ingestion/chunkers/__init__.py` re-exports `CharacterTextChunker`
- **Stage:** `ChunkStage[EnrichedDocument, ChunkedDocument]` in `src/ingestion/stages/chunk.py`
- **Testing:** `tests/unit/ingestion/test_chunking.py`

## [0.1.15] - 2026-09-16

### Added
- **Ingestion context:** `DocumentMetadata` and `EnrichedDocument` in `src/ingestion/context.py` — models for extracted file metadata and enriched documents
- **Metadata:** `MetadataExtractor` base interface in `src/ingestion/metadata.py`; `FilesystemMetadataExtractor` in `src/ingestion/metadata_extractor.py` reading `stat()` fields and markdown headings for the title
- **Stage:** `EnrichStage[CleanedDocument, EnrichedDocument]` in `src/ingestion/stages/enrich.py`
- **Package init:** `src/ingestion/__init__.py` reduced to a module docstring
- **Testing:** `tests/unit/ingestion/test_metadata.py`, `tests/unit/ingestion/test_enrich_stage.py`

## [0.1.14] - 2026-09-16

### Added
- **Ingestion context:** `CleanedDocument` in `src/ingestion/context.py` — Pydantic model for cleaned textual content
- **Cleaning:** `DocumentCleaner` base interface in `src/ingestion/cleaning.py`; `TextDocumentCleaner` in `src/ingestion/cleaners/text.py` normalizing line endings, stripping trailing whitespace, collapsing excessive blank lines, and trimming the content
- **Exports:** `src/ingestion/cleaners/__init__.py` re-exports `TextDocumentCleaner`
- **Stage:** `CleanStage[ParsedDocument, CleanedDocument]` in `src/ingestion/stages/clean.py`
- **Testing:** `tests/unit/ingestion/test_text_cleaner.py`, `tests/unit/ingestion/test_clean_stage.py`

## [0.1.13] - 2026-09-16

### Added
- **Ingestion context:** `ParsedDocument` in `src/ingestion/context.py` — Pydantic model adding a `format` tag to a `RawDocument`
- **Parsers:** `DocumentParser` base interface (`supports`, `parse`) in `src/ingestion/parsers/base.py`; `MarkdownParser` (`.md`, `.markdown`) and `TextParser` (`.txt`) in `src/ingestion/parsers/`
- **Registry:** `ParserRegistry` in `src/ingestion/parsers/registry.py` selects the first supporting parser, raising `ValueError` for unsupported formats
- **Stage:** `ParseStage[RawDocument, ParsedDocument]` in `src/ingestion/stages/parse.py`
- **Exports:** `src/ingestion/parsers/__init__.py` re-exports `DocumentParser`, `MarkdownParser`, `ParserRegistry`, `TextParser`
- **Testing:** `tests/unit/ingestion/test_markdown_parser.py`, `test_parser_registry.py`, `test_parse_stage.py`

## [0.1.12] - 2026-09-16

### Added
- **Ingestion context:** `RawDocument` in `src/ingestion/context.py` — Pydantic model pairing a `DocumentInput` with its loaded `content` and `content_hash`
- **Loaders:** `DocumentLoader` base interface in `src/ingestion/loaders/base.py`; `FilesystemLoader` in `src/ingestion/loaders/filesystem.py` reads UTF-8 text from a filesystem path
- **Exports:** `src/ingestion/loaders/__init__.py` re-exports `DocumentLoader`, `FilesystemLoader`
- **Stage:** `LoadStage[DocumentChange, RawDocument]` in `src/ingestion/stages/load.py`
- **Testing:** `tests/unit/ingestion/test_filesystem_loader.py`, `tests/unit/ingestion/test_load_stage.py`

## [0.1.11] - 2026-09-16

### Added
- **Enum:** `DocumentChangeType` in `src/core/enums.py` (`new`, `modified`, `unchanged`)
- **Hashing:** `calculate_file_hash` in `src/core/hashing.py` — streaming SHA-256 over 1 MiB chunks
- **Ingestion context:** `DocumentChange` in `src/ingestion/context.py` — frozen Pydantic model pairing a `DocumentInput` with `change_type`, `content_hash`, optional `previous_content_hash`
- **Change detection:** `ChangeDetector` in `src/ingestion/change_detection.py` — classifies documents as `NEW` (no previous hash), `MODIFIED` (hash differs), or `UNCHANGED`
- **Testing:** `tests/unit/core/test_hashing.py`, `tests/unit/ingestion/test_change_detection.py` (new/unchanged/modified)

## [0.1.10] - 2026-09-16

### Added
- **Ingestion context:** `DocumentInput` in `src/ingestion/context.py` — frozen Pydantic model (`source`, `source_uri`, `path`) representing a discovered document
- **Sources:** `DocumentSource` base interface in `src/ingestion/sources/base.py`; `FilesystemSource` in `src/ingestion/sources/filesystem.py` with recursive glob-discovery across `*.md`, `*.txt`, `*.pdf`
- **Stages:** Generic `PipelineStage[InputT, OutputT]` base in `src/ingestion/stages/base.py`; `DiscoveryStage` in `src/ingestion/stages/discover.py` running a source's `discover()`
- **Sample data:** `data/raw/billing/sample-policy.md`
- **Testing:** `tests/unit/ingestion/test_filesystem_source.py`, `tests/unit/ingestion/test_discovery_stage.py`

### Known Issues
- `src/ingestion/pipeline.py` still imports the removed `IngestionContext` and `Stage` — awaiting its replacement

## [0.1.9] - 2026-09-16

### Added
- **Service:** `DocumentService` in `src/services/document_service.py` — application service wrapping `DocumentRepository` with commit-aware operations (`create_document`, `get_document`, `get_by_source_uri`, `delete_document`)
- **Exports:** `src/services/__init__.py` re-exports `DocumentService`
- **Testing:** `tests/unit/services/test_document_service.py` covering create/get/delete against the real PostgreSQL test database

### Changed
- **Test fixtures:** `tests/conftest.py` cleanup now runs in teardown via `delete(DocumentDB)` instead of clearing all mapped tables before each test

## [0.1.8] - 2026-09-16

### Added
- **Model:** `DocumentCreate` in `src/models/document.py` — input-only schema with `content_hash` validated via `^[a-fA-F0-9]{64}$`, field-length limits on `source`/`title`/`status`
- **Validation tests:** `test_document_create`, `test_document_rejects_invalid_hash`, `test_document_status_defaults_to_active`
- **Exports:** `src/models/__init__.py` re-exports `DocumentCreate`

### Changed
- **Repository:** `DocumentRepository.create()` now accepts a `DocumentCreate` instead of individual keyword arguments
- **Model constraints:** `Document.content_hash` now uses the same hex-regex pattern as `DocumentCreate`; `source`, `title`, `status` all enforce field-length limits

## [0.1.7] - 2026-09-16

### Added
- **Config loader:** `load_yaml_config()` in `src/config/loader.py` reads YAML files and returns a mapping, raising `FileNotFoundError`/`ValueError` on invalid input
- **Settings:** Layered config in `src/config/settings.py` — `EnvironmentSettings` (pydantic-settings, `.env`-backed), `YamlConfig` (application/logging), top-level `Settings` with `application_name`, `environment_name`, `database_url`, `openrouter_api_key` properties
- **Caching:** `get_settings()` uses `functools.lru_cache` to return a single settings instance
- **Exports:** `src/config/__init__.py` re-exports `Settings` and `get_settings`
- **Dependency:** `pyyaml>=6.0` added to `pyproject.toml`
- **Testing:** `tests/unit/config/test_settings.py`

### Changed
- **DB engine:** `src/db/engine.py` now pulls `DATABASE_URL` from `get_settings()` instead of `os.getenv()`

## [0.1.6] - 2026-09-16

### Added
- **Domain model:** Pydantic `Document` in `src/models/document.py` — `extra="forbid"`, validated `content_hash` (len 64), optional `id`/`created_at`/`updated_at`
- **Model registry:** `src/models/__init__.py` re-exports `Document`
- **Conversion:** `DocumentRepository.to_domain()` maps `DocumentDB` → `Document`; `get_domain_by_id()` returns the application model
- **Testing:** `tests/unit/models/test_document.py`, `test_document_repository_returns_domain_model` integration test

## [0.1.5] - 2026-09-16

### Added
- **Repository:** `DocumentRepository` in `src/db/repositories/documents.py` with `create`, `get_by_id`, `get_by_source_uri`, `get_by_content_hash`, `delete`
- **Fixtures:** Root `tests/conftest.py` with `database_engine` and `database_session` fixtures
- **Testing:** `test_create_and_get_document`, `test_find_document_by_source_uri`, `test_find_document_by_content_hash`

### Changed
- **Test isolation:** `database_session` fixture now clears all rows from mapped tables before each test to prevent `MultipleResultsFound` from accumulated committed data

## [0.1.4] - 2026-09-16

### Added
- **Model:** `DocumentDB` in `src/db/models/document.py` — `documents` table with typed SQLAlchemy 2.x mappings (`id`, `source`, `source_uri`, `title`, `content_hash`, `status`, `created_at`, `updated_at`)
- **Model registry:** `src/db/base.py` imports `DocumentDB` so `Base.metadata` includes the `documents` table for Alembic autogenerate
- **Migration:** `create_documents_table` (`58229e17449f`) creates the `documents` table
- **Testing:** `tests/integration/` with `database_session` fixture (`conftest.py`) and `test_database.py` verifying `DocumentDB` insert + query round-trip

### Changed
- **Migration style:** Auto-fixed Alembic-generated files for ruff compliance

## [0.1.3] - 2026-09-16

### Added
- **Database:** `src/db` module with `base.py` (SQLAlchemy `DeclarativeBase`), `engine.py` (`create_database_engine`), `session.py` (`SessionLocal`)
- **Migrations:** Alembic with `alembic.ini`, `migrations/env.py`, `migrations/versions/`

### Fixed
- **DB Shell:** `db-shell` Makefile target now connects via TCP (`-h localhost -p 5432`) to match the superuser role
- **Alembic:** `load_dotenv()` now runs before app imports in `migrations/env.py` so `DATABASE_URL` is resolved correctly

## [0.1.2] - 2026-09-16

### Added
- **Infra:** Docker Compose (`docker-compose.yml`) with PostgreSQL 17 service, healthchecks, volume `postgres_data`
- **Infra:** Makefile (`Makefile`) with `up`, `down`, `ps`, `logs`, `db-shell` targets
- **Config:** `.env.example` updated with `APP_ENV`, `DATABASE_URL`, `OPENROUTER_API_KEY`

## [0.1.1] - 2026-09-16

### Added
- **Config:** Pydantic settings with `.env` file support and profile loading
- **Core:** Error types (`AetherError`, `ConfigError`, `NotFoundError`), UUID-based ID generation, UTC clock
- **Project scaffold:** `pyproject.toml`, `.env.example`, `.gitignore`, `README.md`, test directory structure

### Changed
- Initial project creation

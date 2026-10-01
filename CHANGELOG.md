# Changelog

All notable changes to `rag-system` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec.php#pec-2.0.0).

## Version History

| Version | Feature Domain | Key Objectives |
|---------|---------------|----------------|
| 0.2.13  | Reliability | `reliability.yaml` + bounded config models, `src/core/exceptions.py` hierarchy, `RetryPolicy` retrying only transient failures, hardened OpenRouter classification and response validation, sanitized API error handlers with `request_id`, `/health/ready`, prompt-injection boundary, `.env.example` |
| 0.2.12  | Observability | `ContextVar` request ID + `X-Request-ID` header, JSON log formatter with token usage, `Timer`, thread-safe `MetricsCollector` shared via a registry singleton, `GET /metrics`, instrumentation of retrieval/generation/RAG |
| 0.2.11  | HTTP API | FastAPI + uvicorn, `create_app()`, `/health` and `POST /rag/query`, request-scoped session dependency, `RAGAPIError` handler, dependency-overridden tests with no network |
| 0.2.10  | RAG Evaluation | `RAGEvaluationCase`/`Result`/`Metrics`, YAML dataset + loader, deterministic `CitationEvaluator`/`GroundingEvaluator`/`SimpleAnswerEvaluator` behind an `AnswerEvaluator` boundary, `RAGEvaluationService`/`Runner`, container wiring, `evaluate_rag` CLI |
| 0.2.9   | RAG Generation | `LLMProvider` contract + `OpenRouterProvider` over `httpx`, `PromptBuilder`, `CitationExtractor`, `GroundingService`; `GenerationService`/`RAGService` returning a cited `RAGResponse`; `config/llm.yaml` with the key kept in `.env` |
| 0.2.8   | Provider Packages | `src/providers/embeddings/` (relocated), `EmbeddingProviderFactory`, provider contract + boundary tests, configured `model_name` |
| 0.2.7   | Composition Root | `ApplicationContainer`, `config/embedding.yaml` + `EmbeddingConfig`, `Settings` flattened; pytest `importlib` import mode fixes collection collisions |
| 0.2.6   | Evaluation Metrics | Stable `(document, chunk_index)` references resolved to chunk IDs against the ACTIVE version; Recall@K/Precision@K/RR/MRR/NDCG@K; YAML dataset loader; 51 tests, all passing |
| 0.2.5   | Reranking | `Reranker` contract + `SimpleReranker`, `RetrievalPipeline` reranking stage, `candidate_k` candidate-pool control |
| 0.2.4   | Hybrid Retrieval | `reciprocal_rank_fusion()` helper, `HybridSearchStrategy` fusing vector + keyword results via RRF |
| 0.2.3   | Keyword Retrieval | PostgreSQL full-text search (`search_vector` TSVECTOR + GIN + trigger), `KeywordSearchRepository`/`KeywordSearchStrategy`, `SearchStrategy` accepts `RetrievalQuery` |
| 0.2.2   | Retrieval Filters | `RetrievalFilter` model unifying `source`/`document_id`/`document_type`; SQL-side filtering via `documents` join, shared embedded-document test factory |
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

## [0.2.13] - 2026-10-01

### Added
- **Reliability configuration:** `config/reliability.yaml` with `llm` (`timeout_seconds`, `max_retries`, `retry_delay_seconds`), `retrieval` (`timeout_seconds`), and `api` (`max_query_length`, `max_top_k`) sections
- **`ReliabilityConfig` models:** `src/config/settings.py` — `LLMReliabilityConfig`, `RetrievalReliabilityConfig`, `APIReliabilityConfig`, and `ReliabilityConfig`, all `extra="forbid"` with bounded fields; exposed as `Settings.reliability` and loaded from `config/reliability.yaml`
- **Application exceptions:** `src/core/exceptions.py` — `RAGSystemError` base with `RetrievalError`, `GenerationError`, `ConfigurationError`, and a `ProviderError` subclass of `GenerationError` covering `ProviderTimeoutError`, `ProviderResponseError`, and `TransientProviderError`. Callers no longer see raw `httpx` or database exceptions
- **`RetryPolicy`:** `src/providers/retry.py` — `execute(operation)` retries a callable up to `max_retries` times with `delay_seconds` between attempts, retrying only `DEFAULT_RETRYABLE` (`ProviderTimeoutError`, `TransientProviderError`). Every other exception propagates on the first attempt
- **OpenRouter failure classification:** `src/providers/llm/openrouter.py` splits the request into `_post` and `_parse`. `_post` maps `httpx.TimeoutException` to `ProviderTimeoutError` and other `httpx.HTTPError` to `TransientProviderError`; HTTP 5xx raises `TransientProviderError` and HTTP 4xx raises `ProviderResponseError`. The response body is never inspected or included in the raised message
- **OpenRouter response validation:** `_parse` rejects non-dict JSON, missing/empty/non-list `choices`, non-dict `message`, and non-string `content` with `ProviderResponseError`, replacing the previous unchecked `data["choices"][0]["message"]["content"]` indexing and `raise_for_status()`
- **Provider retries wired through configuration:** `LLMProviderFactory.create()` accepts an optional `ReliabilityConfig` and builds a `RetryPolicy` from `reliability.llm`; `ApplicationContainer.llm_provider()` passes `self._settings.reliability`. Without a config argument the factory falls back to no retries, so direct construction in tests stays deterministic
- **Prompt-injection boundary:** `PromptBuilder.build_system_prompt()` now instructs the model to treat source content as untrusted data and never to follow instructions contained inside retrieved documents
- **Sanitized API error handlers:** `src/api/errors.py` registers handlers for `ProviderTimeoutError` (504), `RetrievalError` (503), `GenerationError` (502), and `ConfigurationError` (500), each logging a structured event and returning a fixed message. Because provider exceptions subclass `GenerationError`, every provider failure is handled without a handler per class
- **Request IDs in error responses:** all error bodies now include `request_id` from the Phase 6 `ContextVar`, matching the `X-Request-ID` response header
- **Readiness endpoint:** `GET /health/ready` in `src/api/routes/health.py` executes `SELECT 1` through the request-scoped session and returns `{"status": "ready"}`, or `503` with `"Database is unavailable."` on failure. It checks infrastructure only and deliberately makes no LLM call, since a readiness probe would otherwise consume tokens on every check
- **Secret hygiene:** `.gitignore` now ignores `.env.*` while un-ignoring `.env.example`, and a new `.env.example` contains an empty `OPENROUTER_API_KEY=` placeholder
- **Retry tests:** `tests/providers/test_retry.py` (11 — eventual success, immediate success, exhaustion, zero retries, timeouts retried, client errors not retried, transient errors retried, unrelated exceptions not retried, custom retryable sets, and the default set contents)
- **Input-limit tests:** `tests/security/test_input_limits.py` (17 — query length at and beyond the 5000-character limit, empty query, `top_k` bounds, rejection of client-supplied `candidate_k` and `filters`, and two tests proving rejected requests never reach the service)
- **Error-sanitization tests:** `tests/api/test_errors.py` covers readiness success, database failure returning 503, database exception details not leaking, each application exception mapping to its status code, provider error messages not reaching the client, and the error `request_id` matching the response header

### Changed
- **BREAKING:** `LLMConfig.timeout_seconds` is removed. The transport timeout now lives only in `reliability.llm.timeout_seconds`, eliminating two competing sources for the same value. `config/llm.yaml` no longer sets it
- **BREAKING:** `OpenRouterProvider` no longer raises `httpx.HTTPStatusError`. Callers must catch `RAGSystemError` subclasses; `tests/providers/llm/test_openrouter.py` was rewritten with explicit status codes on its mocks and 30 new cases covering classification, redaction, malformed payloads, and retry integration
- `Timer.__exit__` returns early when the context was never entered, keeping `duration_ms` at `0.0` instead of subtracting `None`
- `register_exception_handlers` routes registration through a helper that casts handlers to Starlette's `ExceptionHandler` type at one call site, resolving the five `arg-type` errors mypy reported against `add_exception_handler`
- `OpenRouterProvider` accepts an optional `retry_policy` defaulting to no retries
- **Dependency:** `types-PyYAML` added to the dev group so `mypy src` type-checks the three YAML loader modules instead of reporting missing stubs

### Known Limitations
- **`reliability.api` and `reliability.retrieval` are configured but unused.** `max_query_length` and `max_top_k` duplicate the bounds already hardcoded on `RAGQueryRequest`, and `retrieval.timeout_seconds` is never applied — retrieval has no timeout at all. Two sources of truth that can silently diverge
- **The caches in the performance specification are not implemented.** No `src/cache/` package, no `config/performance.yaml`, no cache keys, no `retrieval.cache_hits`/`generation.cache_hits` counters, and no `tests/performance/`. The database indexes and latency targets from that phase are also outstanding
- **`RetryPolicy` is synchronous and blocking.** `sleep` occupies the request thread, so a 2-retry policy with a 1-second delay can add 2 seconds to a request that already timed out. Retry-After headers are ignored entirely
- **There is no circuit breaker.** Once a provider starts failing, every request still pays the full retry budget; the failure mode is a uniformly slow service rather than a fast one
- **Retries are not idempotency-aware.** A timeout after the provider accepted the request causes a duplicate LLM call, doubling cost for that query with no way to deduplicate
- **Error handlers log at WARNING with the exception type but not the message.** Provider URLs and response bodies are correctly withheld from clients, but the underlying cause is also absent from logs, so diagnosing a repeated failure requires reproducing it
- **`RAGAPIError` remains unraised.** Nothing in the application raises it, so its handler is exercised only by tests
- **`/health/ready` depends on a real database session.** It cannot be tested without a reachable PostgreSQL, and it will fail readiness during a database blip even when the LLM path is healthy — appropriate for a strict probe, but worth knowing before wiring it to a load balancer
- **`test_timer_scales_with_duration` was flaky and was rewritten.** Sleeping 5ms against 2.5ms could invert under scheduler load, since `sleep` guarantees a minimum rather than an exact duration; the replacement compares 10ms against 30ms. This also means the suite currently has no deterministic way to test expiry, since `MemoryCache` reads `monotonic()` directly with no clock seam
- **`mypy src` still reports 3 errors**, all pre-existing and outside this work: two in `src/services/ingestion_persistence_service.py` and one `EnvironmentSettings()` call-arg in `src/config/settings.py`. Verified against a stashed tree

## [0.2.12] - 2026-10-01

### Added
- **Observability package:** `src/observability/` — `context.py`, `logging.py`, `metrics.py`, `timer.py`, plus `registry.py` for the process-wide collector
- **Request correlation:** `src/observability/context.py` — a `ContextVar` request ID with `create_request_id()` (UUID4), `get_request_id()`, and `set_request_id()`. `ContextVar` rather than a global so concurrent requests do not overwrite each other's ID
- **`JsonFormatter`:** `src/observability/logging.py` — emits `level`, `logger`, `message`, and `request_id` when set, then any structured `extra` fields present on the record (`event`, `duration_ms`, `model`, `retrieved_count`, `prompt_tokens`, `completion_tokens`, `total_tokens`, `status_code`, `path`, `method`, `error_type`) plus a formatted `exception` when `exc_info` is set. The field list is a module constant rather than a chain of `hasattr` blocks
- **`configure_logging`:** `src/observability/logging.py` — clears root handlers, installs a stdout `StreamHandler` with `JsonFormatter`, and applies the requested level
- **`Timer`:** `src/observability/timer.py` — a context manager around `perf_counter()` exposing `duration_ms` after exit. `duration_ms` is initialized to `0.0` and `_started_at` to `None` in `__init__`, so reading it inside the block or after an exception does not raise `AttributeError`
- **`MetricsCollector`:** `src/observability/metrics.py` — thread-safe integer counters behind a `Lock`, with `increment(name, value=1)`, `get(name)`, and `snapshot()` returning a copy so callers cannot mutate internal state
- **Metrics registry:** `src/observability/registry.py` — `get_metrics()` returns a lazily created double-checked-locked singleton, with `set_metrics()` and `reset_metrics()` for tests
- **`ApplicationContainer.metrics`:** a property returning the shared collector, passed into `RetrievalPipeline`, `GenerationService`, and `RAGService`
- **Retrieval instrumentation:** `RetrievalPipeline.execute()` now times search plus reranking, increments `retrieval.requests`, increments `retrieval.empty_results` when nothing is retrieved, and logs `retrieval.completed` with `duration_ms` and `retrieved_count`
- **Generation instrumentation:** `GenerationService.generate()` increments `generation.requests`, wraps the provider call in a `Timer`, increments `generation.errors` and logs `generation.failed` with `logger.exception` on provider failure before re-raising, and logs `generation.completed` with `duration_ms`, `model`, and all three token counts
- **Request instrumentation:** `RAGService.answer()` increments `rag.requests`
- **Observability middleware:** `src/api/app.py` creates a request ID per HTTP request, times the downstream call, sets an `X-Request-ID` response header, and logs `http.request.completed` with `duration_ms`, `method`, `path`, and `status_code`
- **Startup configuration:** `create_app()` calls `configure_logging(settings.logging.level)`, reusing the existing `logging: level: INFO` configuration
- **Metrics endpoint:** `GET /metrics` in `src/api/routes/metrics.py`, returning the collector snapshot and injected through `get_metrics_collector` rather than a module global
- **Observability tests:** `tests/observability/test_context.py` (6 — correlation round-trip, `set_request_id`, uniqueness, UUID validity, and a subprocess check that the default really is `None`), `tests/observability/test_timer.py` (6 — positive duration, duration scales with elapsed time, and duration recorded even when the block raises), `tests/observability/test_metrics.py` (12 — counting, custom increments, missing keys, snapshot isolation, and registry singleton/`set`/`reset` behavior)

### Changed
- `RetrievalPipeline.execute()` no longer returns early when no reranker is configured; search and reranking share one `Timer`, so the logged duration covers the whole retrieval path rather than only the search call

### Known Limitations
- **`rag.errors` and `rag.errors`-style top-level error counting are not implemented.** `generation.errors` covers provider failures only; retrieval and end-to-end failures still propagate without a counter
- **`retrieval.requests` counts executions, not successes.** A retrieval that raises increments the counter before propagating, so the metric cannot distinguish attempted from completed retrievals
- **The metrics collector is process-local.** Counters reset on restart and are not shared across uvicorn workers, so a multi-worker deployment will report per-worker totals that do not sum to true traffic. Exporting to Prometheus or OpenTelemetry, which the collector was designed to be replaced by, is still outstanding
- **`/metrics` returns only counters that have been incremented.** A fresh process reports `{}`, with no zero-initialized baseline for the documented metric names
- **`JsonFormatter` reads a fixed allow-list of `extra` fields.** Any structured field outside `_STRUCTURED_FIELDS` is silently dropped from the JSON payload, so new instrumentation fields require editing the constant
- **`configure_logging()` clears root handlers each time `create_app()` runs.** Tests calling `create_app()` repeatedly mutate global logging state, and any other handler installed by an embedding application is removed
- **Logging is configured as a side effect of building the app.** `create_app()` is not side-effect free, which slightly undercuts its value as a pure test factory

## [0.2.11] - 2026-10-01

### Added
- **FastAPI and uvicorn:** added as runtime dependencies; `httpx` was already a runtime dependency, so it was not duplicated into the dev group for `TestClient`
- **API package:** `src/api/` — `app.py` with `create_app()` plus a module-level `app` for `uvicorn src.api.app:app --reload`, `dependencies.py`, `errors.py`, and `routes/` holding the `health` and `rag` routers
- **API schemas:** `src/models/api.py` — `RAGQueryRequest(query, top_k=5)` bounded to `1..5000` characters and `top_k` in `[1, 20]` with `extra="forbid"`, and `RAGQueryResponse` mirroring `RAGResponse`. The HTTP schema is deliberately separate from `RetrievalQuery`, keeping the boundary HTTP schema → application schema → domain services
- **`get_db_session`:** `src/api/dependencies.py` — a `Generator[Session]` yielding `SessionLocal()` and closing it in `finally`, so request-scoped sessions are cleaned up
- **`get_rag_service`:** `src/api/dependencies.py` — depends on `get_db_session`, builds `ApplicationContainer`, and returns `container.rag_service()`, keeping all composition in the container rather than in the route
- **Health endpoint:** `GET /health` returning `{"status": "ok"}`; no database or provider checks yet
- **RAG endpoint:** `POST /rag/query` — validates the request, builds `RetrievalQuery(query, top_k)`, calls `RAGService.answer()`, and projects the result onto `RAGQueryResponse`. The endpoint holds no retrieval or generation logic
- **`RAGAPIError`:** `src/api/errors.py` — carries `message` and `status_code` (default `500`); `register_exception_handlers(app)` renders it as `{"error": message}`. Registered in `create_app()`. Unexpected exceptions are deliberately left unmasked
- **API tests:** `tests/api/test_health.py` (1), `tests/api/test_rag.py` (7 — response shape, `top_k` forwarding, the `top_k=5` default, empty query, unknown field, out-of-range `top_k`, and OpenAPI generation), `tests/api/test_errors.py` (4 — status code and body, the `500` default, unexpected errors staying unmasked, and health still working with handlers registered). The RAG route tests override `get_rag_service`, so no test reaches OpenRouter
- **Lint configuration:** `pyproject.toml` gained a `[tool.ruff.lint.per-file-ignores]` entry scoping `B008` to `src/api/*`, because `Depends()` in an argument default is FastAPI's dependency-injection idiom rather than a mutable-default bug

### Changed
- Verified live with `uvicorn src.api.app:app`: `/health` returns `{"status":"ok"}`, and the OpenAPI schema exposes exactly `/health` and `/rag/query`

### Known Limitations
- **`POST /rag/query` still returns `500` in this environment, for two stacked reasons.** `OPENROUTER_API_KEY` is empty in `.env`, so `get_rag_service` raises during dependency resolution and masks request validation — an empty `query` body returns `500` instead of `422`. Once a key is present, validation returns `422` correctly (confirmed in-process), and a valid request then fails with `ValueError: No active index version exists` because the database holds zero documents and no index versions
- **Dependency construction failure shadows `422` validation.** FastAPI resolves `get_rag_service` before the endpoint body is validated, so any configuration error surfaces as `500` for *every* request to `/rag/query`, including malformed ones. A `/health/ready` endpoint that reports configuration and database state would make this diagnosable instead of a stack trace
- **`get_db_session` is unexercised by tests.** Every route test overrides `get_rag_service`, so session creation and cleanup have no coverage; a test asserting the generator closes its session would close that gap
- **`RAGQueryResponse` has no error envelope for retrieval failures.** Because `RAGAPIError` is defined but never raised anywhere, the error path exists only as a mechanism — no service currently translates domain failures (missing active version, provider errors) into it
- **No request timeouts, authentication, rate limiting, or CORS configuration**, and the synchronous `def` route handlers run in the threadpool, so a slow provider call occupies a worker for the full `timeout_seconds`

## [0.2.10] - 2026-10-01

### Added
- **RAG evaluation models:** `src/models/rag_evaluation.py` — frozen, `extra="forbid"` `RAGEvaluationCase(case_id, query, reference_answer, expected_citations)`, `RAGEvaluationResult`, and `RAGEvaluationMetrics`, every score bounded to `[0.0, 1.0]` so per-case and aggregate metrics cannot drift out of range
- **Evaluation dataset:** `data/evaluation/rag_v1.yaml` — version 1 with three deliberately simple cases (billing dispute, refund window, compromised account). Reference answers describe the expected fact generically rather than asserting it, and each expects `SOURCE-1`
- **`RAGEvaluationDatasetLoader`:** `src/evaluation/rag_dataset_loader.py` — `load()` returning `(version, cases)` with `FileNotFoundError` for a missing path and distinct `ValueError` messages for a non-mapping root, non-integer version, non-list cases, and an empty case list; validates every case through `RAGEvaluationCase`
- **`CitationEvaluator`:** `src/evaluation/citation/evaluator.py` — deterministic set comparison of `expected_citations` against the citations actually attached to a `RAGResponse`, returning `(precision, recall)` as `|expected ∩ actual| / |actual|` and `/ |expected|`; no LLM is involved
- **`GroundingEvaluator`:** `src/evaluation/grounding/evaluator.py` — conservative structural check scoring `1.0` only when the answer is non-empty, something was retrieved, and at least one citation is attached; measures citation *support structure*, not semantic faithfulness
- **`AnswerEvaluator` boundary:** `src/evaluation/answer/base.py` — abstract `evaluate(case, response) -> float`, so the deterministic baseline can be swapped for an LLM-as-judge without touching the service
- **`SimpleAnswerEvaluator`:** `src/evaluation/answer/semantic.py` — baseline token-overlap score, `|reference_tokens ∩ answer_tokens| / |reference_tokens|` over case-folded `\b\w+\b` tokens
- **`RAGEvaluationService`:** `src/services/rag_evaluation_service.py` — `evaluate_case()` answers each case through `RAGService` and runs all three evaluators; `evaluate()` raises `ValueError` on an empty case list and otherwise reports the unweighted arithmetic mean of each metric
- **`RAGEvaluationRunner`:** `src/evaluation/rag_evaluation_runner.py` — loads a dataset path and returns `(version, metrics)`, so callers own dataset selection
- **Evaluation CLI:** `src/cli/evaluate_rag.py` — `uv run python -m src.cli.evaluate_rag [--dataset PATH]`, defaulting to `data/evaluation/rag_v1.yaml`; prints dataset version and the four scores
- **Container wiring:** `ApplicationContainer.rag_evaluation_service()` builds the service from `RAGService` plus the three evaluators, completing the CLI → container → `RAGEvaluationService` → `RAGService` → retrieval + generation flow
- **Evaluator tests:** `tests/evaluation/test_citation_evaluator.py` (7 tests: exact match, wrong citation, partial overlap, extra generated citation lowering precision, no citations, no expectations either side, and no expectations with a generated citation), `tests/evaluation/test_grounding_evaluator.py` (5), `tests/evaluation/test_answer_evaluator.py` (9, including the reference-token denominator, case-insensitivity, and that `AnswerEvaluator` is abstract)
- **Loader, runner, and service tests:** `tests/evaluation/test_rag_dataset_loader.py` (9, including the shipped dataset loading as three cases), `tests/evaluation/test_rag_evaluation_runner.py` (3), `tests/services/test_rag_evaluation_service.py` (5, using a fake `RAGService` plus fake evaluators to pin averaging and the empty-case guard)
- **End-to-end evaluation test:** `tests/evaluation/test_rag_evaluation_end_to_end.py` runs the real loader, runner, service, and all three real evaluators over the shipped dataset with only `RAGService` replaced — proving perfect scores for correctly cited verbatim answers, near-zero relevance for uncited off-topic answers, and grounding `0.0` when nothing was retrieved

### Known Limitations
- **The CLI cannot currently run end to end in this environment.** `OPENROUTER_API_KEY` is present but empty in `.env`, and the database holds zero documents and zero index versions, so `ApplicationContainer.rag_evaluation_service()` fails fast on the missing key before any evaluation happens. Both are environment gaps, not code defects; the wiring is covered by tests instead
- **`expected_citations` are positional.** Every shipped case expects `SOURCE-1`, so citation precision measures whether the first-ranked chunk is the right one. Any retrieval-ranking change silently rescores the metric rather than failing, and a correct answer citing `SOURCE-2` is scored as fully wrong. Keying expectations on stable chunk or document identity — as retrieval evaluation already does via `EvaluationChunkReference` — would make this robust to ranking
- **A fabricated citation with nothing retrieved still scores perfect precision and recall.** Citation metrics read only the `citations` list and never consult `retrieved_count`, so `grounding` is the only signal that catches it; `tests/evaluation/test_rag_evaluation_end_to_end.py::test_grounding_zero_when_nothing_was_retrieved` pins that split deliberately
- **`SimpleAnswerEvaluator` is a weak proxy.** It scores reference-token recall over unfiltered `\b\w+\b` tokens, so stopwords count as overlap and a short answer containing every reference word scores `1.0` while being far less complete than the reference. It is a baseline for regression tracking, not a correctness measure
- **Per-case results are discarded.** `RAGEvaluationService.evaluate()` computes each `RAGEvaluationResult` and immediately reduces to means, so the CLI cannot show which case regressed without a code change; only aggregate scores are observable
- **Two independent notions of grounding now exist.** `GroundingService` (in production, from `0.2.9`) and `GroundingEvaluator` (in evaluation) apply similar rules while living in separate layers, and the production result is still discarded. Consolidating them is deferred until the LLM-as-judge work lands
- **`top_k` is not configurable per case.** `evaluate_case()` builds `RetrievalQuery(query=case.query)` and takes the default, so a dataset cannot exercise a different retrieval depth

## [0.2.9] - 2026-10-01

### Added
- **`httpx` dependency:** added in place of a vendor SDK, so the application depends on `LLMProvider` and plain HTTP rather than an OpenRouter client
- **LLM configuration file:** `config/llm.yaml` — `provider: openrouter`, `model: openai/gpt-oss-20b:free`, `temperature: 0.0`, `max_tokens: 1000`, `timeout_seconds: 60`; the API key stays in `.env` as `OPENROUTER_API_KEY`, keeping secrets out of configuration
- **`LLMConfig`:** `src/config/settings.py` — `extra="forbid"` with bounded `provider`/`model`, `temperature` in `[0.0, 2.0]`, `max_tokens` in `(0, 100_000]`, and `timeout_seconds` in `(0, 300]`, exposed as `Settings.llm` and loaded from `config/llm.yaml` through the existing YAML loader
- **RAG response models:** `src/models/rag.py` — frozen, `extra="forbid"` `Citation(citation_id, document_id, chunk_id, chunk_index)` and `RAGResponse(query, answer, citations, model_name, retrieved_count)`. Retrieval internals (`RetrievalResult`) stay internal; the API and CLI only ever see the user-facing citation shape
- **`PromptBuilder`:** `src/generation/prompt_builder.py` — owns the system prompt (grounding rules plus the `[SOURCE-N]` citation contract) and assembles the user prompt from numbered sources and the question, keeping prompts in Python until they move into the prompt registry
- **`CitationExtractor`:** `src/generation/citations.py` — resolves `[SOURCE-N]` markers in an answer back to the retrieved chunk that produced them, deduplicating repeats, ignoring markers that point outside the retrieved set, and preserving first-appearance order
- **`GroundingService`:** `src/services/grounding_service.py` — `validate(answer, citation_count)` returning a typed `GroundingResult(grounded, citation_count)`; an empty answer is never grounded, and a non-empty answer requires at least one citation
- **Generation models:** `src/models/generation.py` — frozen, `extra="forbid"` `GenerationRequest(query, system_prompt, user_prompt)` and `GenerationResponse(answer, model_name, prompt_tokens, completion_tokens, total_tokens)` with optional token usage, so the application never sees OpenRouter's response schema
- **`LLMProvider` interface:** `src/providers/llm/base.py` — `model_name` and `generate(GenerationRequest)`, making the LLM a swappable dependency rather than an OpenRouter dependency
- **`OpenRouterProvider`:** `src/providers/llm/openrouter.py` — posts the request's pre-built system and user messages to the chat completions endpoint over `httpx`; extracts the answer and optional usage, prefers the model reported by the response and falls back to the configured name, and lets HTTP and transport errors propagate. It carries no prompt text of its own, so prompt wording changes never touch the transport layer
- **`LLMProviderFactory`:** `src/providers/llm/factory.py` — `create(LLMConfig, api_key)` normalizes the provider name with `strip().lower()`, raises `ValueError` for unsupported providers, and requires a non-empty API key for OpenRouter
- **`ContextBuilder`:** `src/generation/context_builder.py` — renders retrieved chunks into a source-labelled context carrying full provenance (`Document ID`, `Chunk ID`, `Chunk Index`) per source, preserving result order and joining sections with a blank line
- **`GenerationService`:** `src/services/generation_service.py` — builds both prompts, delegates to the provider, extracts citations from the answer, and returns a `RAGResponse`; short-circuits to a "could not find relevant information" response when retrieval returns nothing so no LLM call is made without grounding
- **`RAGService`:** `src/services/rag_service.py` — the end-to-end flow, running `RetrievalPipeline.execute()` and passing the results into generation, exposing a single `answer(RetrievalQuery) -> RAGResponse` so the top-level contract is `RetrievalQuery` in, `RAGResponse` out
- **LLM container wiring:** `ApplicationContainer` gained `llm_provider()`, `generation_service()`, and `rag_service()`, so the whole RAG application is constructible from one composition root
- **Citation and grounding tests:** `tests/generation/test_citations.py` (single/multiple markers, out-of-range markers ignored, deduplication, absent markers, first-appearance ordering), `tests/services/test_grounding_service.py` (cited answer grounded, empty and whitespace answers not grounded, uncited answer not grounded), `tests/generation/test_prompt_builder.py` (citation format in the system prompt, numbered sources and question in the user prompt, ordering, empty sources)
- **LLM tests (no network):** `tests/providers/llm/test_openrouter.py` mocks `httpx.Client` to cover answer extraction, usage extraction and its absence, response-model preference and fallback, model/temperature/`max_tokens` payload construction, API key and endpoint wiring, message contents, timeout application, and HTTP/transport error propagation (12 tests); `tests/providers/llm/test_factory.py` covers provider creation, name normalization, API key requirements, unsupported providers, and provider-name validation preceding key validation (6 tests)
- **Generation tests:** `tests/services/test_generation_service.py` (citation extraction, query echo and counts, citation-to-chunk mapping, pre-built prompt delivery, uncited answers, and the no-context fallback that skips the provider call), `tests/services/test_rag_service.py` (end-to-end retrieval → generation → citations against a fake pipeline and fake provider, `top_k` forwarding, correct source mapping, and both empty-result and no-citation paths), `tests/generation/test_context_builder.py` (source markers, provenance fields, ordering, section separation)

### Changed
- **BREAKING:** `GenerationRequest.context` is replaced by `system_prompt` and `user_prompt`, moving prompt construction out of `OpenRouterProvider` — the provider now only marshals pre-built messages and owns no prompt policy
- `GenerationService.generate()` returns `RAGResponse` instead of `GenerationResponse`, and `RAGService.answer()` is typed against it; `GenerationResponse` remains the internal provider-boundary type
- `ApplicationContainer.generation_service()` gained `prompt_builder`, `citation_extractor`, and `grounding_service` dependencies alongside the existing provider and context builder
- `Settings` gained a required `llm: LLMConfig` field, so `config/llm.yaml` must exist for `get_settings()` to succeed — the same load-time validation path as `config/embedding.yaml`
- `ApplicationContainer.rag_service()` requires `OPENROUTER_API_KEY` to be set: `llm_provider()` raises `ValueError` when the key is absent or empty, so the composition root deliberately fails fast instead of deferring the failure to the first query

### Known Limitations
- **`GroundingService` output is currently discarded.** `GenerationService.generate()` calls `validate()` and drops the returned `GroundingResult`, so `grounded` is never surfaced on `RAGResponse`, logged, or enforced. The check exists as a boundary but has no effect on behavior until something observes it
- **`ContextBuilder` is injected but unused.** `PromptBuilder.build_user_prompt()` formats its own `[SOURCE-N]` blocks, so the `Document ID` / `Chunk ID` / `Chunk Index` provenance that `ContextBuilder` renders never reaches the model — the LLM sees only the source marker and the chunk text. Two components format sources independently and can drift; `tests/generation/test_context_builder.py` is the only thing exercising it
- **Citations cannot be verified as *correct*, only as *well-formed*.** `CitationExtractor` maps `[SOURCE-N]` to `results[N-1]`, so a marker pointing outside the retrieved set is rejected, but a model citing the wrong in-range source still produces a confidently incorrect `Citation`. Detecting that requires entailment checking, not pattern matching

## [0.2.8] - 2026-10-01

### Added
- **`EmbeddingProviderFactory`:** `src/providers/embeddings/factory.py` — `create(EmbeddingConfig)` maps a configured `provider` name to a concrete provider and raises `ValueError` for anything unsupported; `local` is the only branch today, but the extension point exists before any external provider is added
- **Provider contract tests:** `tests/providers/embeddings/test_contract.py` — a `LocalEmbeddingProvider` fixture exercised through the `EmbeddingProvider` interface for metadata, batch embedding (one vector per text), query embedding, the `[] -> []` empty-batch policy, agreement between `embed_query` and `embed`, and the dimension invariant that ties `provider.dimensions` to the pgvector/index-version dimension (7 tests)
- **Provider boundary tests:** `tests/providers/embeddings/test_embedding_integration.py` — configuration → factory → provider end to end, asserting configured dimensions survive into the produced vectors for both batch and query embedding (3 tests)

### Changed
- **BREAKING:** `src/embeddings/` is relocated to `src/providers/embeddings/` (`base`, `local`, `factory`), matching the layout used by the new factories and future external providers; all importers were updated (`ingestion.factory`, `ingestion.pipeline`, `ingestion.stages.embed`, `services.reindex_service`, `application.container`, and the corresponding tests)
- **BREAKING:** `LocalEmbeddingProvider` now accepts `model_name: str = "local-dev"` and returns it from the `model_name` property, so the configured `embedding.yaml` model name reaches the provider through the factory instead of the hardcoded `"local-deterministic"` string; the default changed, so `test_embedding_model_metadata` and `test_embed_stage` assert `"local-dev"` now
- **BREAKING:** `embed_query` moved from a concrete default on `EmbeddingProvider` to an abstract method implemented by each provider, making single-query embedding an explicit part of every provider contract; every subclass and test double must now implement it
- `EmbeddingProviderFactory.create()` normalizes the configured provider name with `strip().lower()`, so `LOCAL` and `"  local  "` resolve to the same provider while unknown names — including a whitespace-only value that passes the `min_length=1` field constraint — still raise `ValueError`
- `ApplicationContainer.embedding_provider()` no longer knows how providers are built — it delegates to a single `EmbeddingProviderFactory` instance created in the constructor, so adding a provider means editing the factory and nothing else
- Provider tests moved from `tests/unit/embeddings/` to `tests/providers/embeddings/` to mirror the source layout, alongside the new `test_factory.py` (5 tests)

## [0.2.7] - 2026-10-01

### Added
- **`ApplicationContainer`:** `src/application/container.py` — a plain composition root holding the `Session` and `Settings` and exposing factory methods for each repository (`document`, `chunk`, `embedding`, `index_version`, `vector_search`, `keyword_search`), the embedding provider, the hybrid `RetrievalService`, the `RetrievalPipeline`, the `EvaluationResolver`, and the `RetrievalEvaluationRunner`. Deliberately hand-written rather than a dependency-injection framework, so construction stays explicit and greppable
- **Embedding configuration file:** `config/embedding.yaml` — `provider: local`, `model: local-dev`, `dimensions: 8`; `local` is the deterministic development provider, so the vector dimension is now declared in configuration instead of hardcoded
- **`EmbeddingConfig`:** `src/config/settings.py` — `extra="forbid"` with `provider` capped at 100 characters, `model` at 200, and `dimensions` constrained to `> 0`, exposed as `Settings.embedding`; `embedding.yaml` is parsed by the existing `load_yaml_config` and validated once at load time, with no YAML parsing duplicated inside the provider
- **Container tests:** `tests/application/test_container.py` — repository, retrieval pipeline, evaluation runner, and embedding-provider construction against a `MagicMock` session, plus dimensions sourced from settings and rejection of an unsupported provider name; these verify composition only, not PostgreSQL behavior (6 tests)
- **Configuration tests:** `tests/unit/config/test_settings.py` gained `test_settings_load_embedding_config` and rejection tests for a misspelled `dimension` field, non-positive dimensions, and an empty provider name

### Changed
- **BREAKING:** `Settings` is flattened from `environment` + nested `yaml: YamlConfig` to explicit `environment`, `application`, `logging`, and `embedding` fields (the now-unused `YamlConfig` wrapper is removed), so each YAML file maps to one field on `Settings`; the `application_name`/`environment_name`/`database_url` accessors are unchanged for existing callers
- `ApplicationContainer` now requires `settings` and builds its embedding provider from `Settings.embedding` instead of a hardcoded 8 dimensions, rejecting any provider other than `local` with a `ValueError`

### Fixed
- **Test collection:** `uv run pytest` aborted during collection with `import file mismatch` because `tests/evaluation/metrics/test_retrieval.py`, `tests/models/test_retrieval.py`, and two other pairs shared a module basename while their directories were not importable packages. `pyproject.toml` now sets `addopts = "--import-mode=importlib"`, which derives module names from each file's path and fixes all three collisions at once instead of renaming test files or restructuring the test tree
- **Stale retrieval filters in tests:** `tests/services/test_retrieval_service.py` still passed `source`/`document_id` directly to `RetrievalQuery`, which now requires a `RetrievalFilter` via `filters`; both filter tests pass again

## [0.2.6] - 2026-09-25

### Added
- **Evaluation models:** `EvaluationChunkReference`, `RetrievalEvaluationCase`, and `RetrievalEvaluationResult` in `src/models/retrieval_evaluation.py` — a stable `(document, chunk_index)` reference, a ground-truth case (`case_id`, `query`, `relevant_chunks`), and a comparable outcome (`case_id`, `retrieved_chunk_ids`, `relevant_chunk_ids`), all frozen with `extra="forbid"`
- **Stable chunk references:** relevance is expressed as `EvaluationChunkReference(document, chunk_index)` on the *dataset* instead of database chunk UUIDs, so an evaluation dataset survives reindexing and does not encode storage-layer identifiers; relevance is resolved back to UUIDs only when a `RetrievalEvaluationResult` is constructed, keeping every result in one comparable UUID space
- **`RetrievalEvaluationService`:** `src/services/retrieval_evaluation_service.py` — `evaluate_case(case, results)` builds a `RetrievalEvaluationResult` from retrieval output and the ground-truth case, resolving the case's stable references through an injected `EvaluationResolver` so metrics can be computed without re-running retrieval
- **Evaluation package:** `src/evaluation/` with `src/evaluation/metrics/retrieval.py`
- **`RecallAtK`:** fraction of relevant chunks found in the top-`k` retrieved chunks; empty relevance set returns `0.0`, `k <= 0` raises `ValueError`
- **`PrecisionAtK`:** fraction of the top-`k` retrieved chunks that are relevant; empty result set returns `0.0`, `k <= 0` raises `ValueError`
- **`ReciprocalRank`:** reciprocal of the rank of the first relevant chunk within the top `k` (`1/rank`), returning `0.0` when no relevant chunk appears; `k <= 0` raises `ValueError`
- **`MeanReciprocalRank`:** dataset-level MRR — averages `ReciprocalRank` over a list of `RetrievalEvaluationResult`s (`sum(rr) / len(results)`), returning `0.0` for an empty dataset; `k <= 0` raises `ValueError`
- **`NDCGAtK`:** binary-gain NDCG@K — `DCG@K / IDCG@K` with gain `1/log2(rank+1)` and an ideal ranking of `min(k, len(relevant))` relevant chunks; returns `0.0` when nothing relevant was retrieved, `0.0` for an empty relevance set, and raises `ValueError` for `k <= 0`
- **`RetrievalMetrics` model:** `src/models/retrieval_metrics.py` — frozen, `extra="forbid"` summary of `recall_at_k`, `precision_at_k`, `mrr`, `ndcg_at_k`, each constrained to `[0.0, 1.0]`
- **`RetrievalMetricsService`:** `src/services/retrieval_metrics_service.py` — `evaluate(evaluations, k)` runs the four metrics over a dataset and returns a single `RetrievalMetrics`; empty datasets yield all-zero metrics, `k <= 0` raises `ValueError`
- **`EvaluationResolver`:** `src/services/evaluation_resolver.py` — resolves `EvaluationChunkReference(document, chunk_index)` into an indexed `chunk_id` by looking up the document by `source_uri` and scanning that document's chunks within the **active** index version; `resolve_all()` maps a list of references. Raises `RuntimeError` when no ACTIVE version exists and `LookupError` when the document or the specific chunk index is absent, with the resolved version number in the message
- **`RetrievalEvaluationRunner`:** `src/services/retrieval_evaluation_runner.py` — end-to-end entry point that turns `RetrievalEvaluationCase`s into live `RetrievalPipeline.execute()` calls (`top_k=k`), resolves each case's stable references via the injected `EvaluationResolver`, maps each response to a `RetrievalEvaluationResult`, and delegates aggregation to `RetrievalMetricsService`
- **`RetrievalEvaluationDataset` model:** `src/models/retrieval_evaluation_dataset.py` — frozen, `extra="forbid"` wrapper pairing a `version` (`ge=1`) with a non-empty `cases` list, so a dataset file is schema-validated before it reaches the application layer
- **`RetrievalEvaluationDatasetLoader`:** `src/evaluation/dataset_loader.py` — `load(path)` reads YAML via `yaml.safe_load`, raises `FileNotFoundError` for a missing path and `ValueError` when the root is not a mapping, then returns a validated `RetrievalEvaluationDataset`
- **Evaluation dataset:** `data/evaluation/retrieval_v1.yaml` — three seed cases (billing dispute, refund window, account compromise) referencing chunks by `document` + `chunk_index`; the document paths and chunk indexes are examples to be confirmed against the real evaluation corpus
- **Testing:** `tests/services/test_evaluation_resolver.py` (successful resolution, missing document, missing chunk index, no active version, batch resolution + order preservation + empty list, and version scoping — all against fake repositories, no PostgreSQL required); `tests/evaluation/test_dataset_loader.py` (valid load, missing file, non-mapping root, empty case list, unknown field rejection, and the shipped dataset parsing); `tests/services/test_retrieval_evaluation_service.py` (case→result mapping including resolver delegation), `tests/services/test_retrieval_metrics_service.py` (all-metrics, empty dataset, invalid `k`), `tests/services/test_retrieval_evaluation_runner.py` (single case + request assertions, multi-case aggregation, stable-reference resolution delegated to the resolver, retrieved-vs-resolved scoring, invalid `k`, empty case list), and `tests/evaluation/metrics/test_retrieval.py` (26 tests: 6 per metric, plus MRR averaging/empty-dataset and NDCG ideal/partial/miss/position-sensitivity cases) — 51 tests total

### Changed
- **BREAKING:** `RetrievalEvaluationCase.relevant_chunk_ids` is replaced by `relevant_chunks: list[EvaluationChunkReference]`; `RetrievalEvaluationResult.relevant_chunk_ids` keeps its name but is now populated by `EvaluationResolver.resolve_all()` rather than being authored by hand. Relevance is therefore stable on the dataset and UUID-based on the result, and metric implementations read a single comparable UUID space again
- `RetrievalEvaluationRunner` and `RetrievalEvaluationService` now require an `EvaluationResolver` constructor argument — resolution is an explicit dependency rather than an implicit lookup, and a dataset referencing a chunk that no longer exists fails the run loudly via `LookupError` instead of silently scoring `0.0`
- Resolution deliberately does not keep the stable references alongside the resolved IDs on the result: two representations of "what was relevant" could disagree, and the references remain authoritative on the dataset (which is version-controlled) for traceability
- Raw `retrieved_chunk_ids`/`relevant_chunk_ids` pairs are the single metric input, so all metrics share one comparable result shape and no retrieval re-execution is needed per metric
- `MeanReciprocalRank` is the first metric consuming a *list* of results, setting the pattern for dataset-level aggregates
- `RetrievalMetricsService` owns the metric instances and exposes one `evaluate()` call, so callers never construct metrics directly or hand-average scores
- Metric aggregation is unweighted macro-averaging over cases (each case counts equally), matching the existing per-case metric definitions
- The runner validates `k` before issuing any retrieval call, so a bad `k` fails fast with the project's `ValueError` message instead of surfacing later as a Pydantic `top_k` constraint error
- Evaluation datasets are validated at load time, so malformed YAML fails at the boundary instead of producing silently wrong metric scores

## [0.2.5] - 2026-09-25

### Added
- **Reranking:** `Reranker` abstract base class (`src/retrieval/rerank/base.py`) with a `rerank()` contract; `SimpleReranker` development implementation (`src/retrieval/rerank/simple.py`) that preserves the incoming ranking while enforcing `top_k`
- **Pipeline reranking:** `RetrievalPipeline` now optionally accepts a `Reranker` and applies reranking after retrieval (`src/retrieval/pipeline.py`)
- **`candidate_k` field:** `RetrievalQuery` now carries an optional `candidate_k` (`int | None`, 1–500) controlling the candidate pool size before reranking/fusion; when `None`, falls back to `top_k * candidate_multiplier` (`src/models/retrieval.py`)
- **Testing:** `tests/retrieval/rerank/test_simple.py` — simple reranker order/`top_k`/validation tests; `tests/retrieval/test_pipeline.py` — pipeline reranking test with `FakeReranker`

### Changed
- `RetrievalService.search()` unchanged — it still returns the candidate pool; the pipeline layer applies reranking
- `HybridSearchStrategy` candidate counting now respects `candidate_k` before truncating to `top_k`

## [0.2.4] - 2026-09-25

### Added
- **Reciprocal Rank Fusion helper:** `reciprocal_rank_fusion()` in `src/retrieval/search/base.py` for combining multiple ranked result lists
- **`HybridSearchStrategy`:** a `SearchStrategy` implementation that fuses vector and keyword search results using RRF
- **Diversified retrieval:** `HybridSearchStrategy` supports `fusion_k` and `candidate_multiplier` parameters controlling search scope and fusion behavior

### Changed
- `reciprocal_rank_fusion()` is a reusable utility that can be used independently or by `HybridSearchStrategy`
- `HybridSearchStrategy.search()` first expands results by `candidate_multiplier` before fusion so enough candidates are considered before returning the top `top_k` results

## [0.2.3] - 2026-09-25

### Added
- **PostgreSQL full-text search:** `search_vector` column (TSVECTOR) added to the `chunks` table with a GIN index
- **Full-text search trigger:** automatic `search_vector` population on chunk insert/update via a PostgreSQL trigger function
- **`KeywordSearchRepository`:** `search()` using `websearch_to_tsquery` / `ts_rank_cd` against `search_vector`
- **`KeywordSearchStrategy`:** new `SearchStrategy` implementation for PostgreSQL full-text search
- **Pipeline diversification:** `RetrievalService` now accepts any `SearchStrategy` (vector or keyword), decoupling search logic from the service layer
- **Document type field:** `document_type` column added to the `documents` table (String(100), nullable), and to both `DocumentCreate` and `Document` with `max_length=100`
- **Document type filtering:** `RetrievalQuery` carries an optional `document_type` filter, applied in SQL via `DocumentDB.document_type`; `document_type` flows from `EnrichedDocument.metadata` through `DocumentCreate` → `DocumentDB` → persistence
- **Repository methods:** `DocumentRepository.create()` and `update_content_hash()` persist `document_type`; `to_domain()` converts it to the application model

### Changed
- `SearchStrategy` base class now accepts `RetrievalQuery` instead of separate query vector / `top_k` / filters parameters
- `VectorSearchStrategy.search()` and `KeywordSearchStrategy.search()` take `RetrievalQuery`, delegating embedding to the `EmbeddingProvider` and query processing to `KeywordSearchRepository`
- `RetrievalService` constructor accepts `search_strategy` instead of `vector_search_repository` + `embedding_provider`
- `ChunkDB` includes `search_vector: Mapped[str | None] = mapped_column(TSVECTOR, nullable=True)`
- `RetrievalService.search()` forwards the requested filters to the repository for SQL-side filtering
- `DocumentRepository.update_content_hash()` also updates `document_type`, clearing it when metadata reports `None`

### Fixed
- `search_vector` is maintained by trigger, so the tsvector is always in sync with `content`
- Metadata refresh: when newly extracted metadata has `document_type=None`, the previous value is now cleared (previously only `title` was non-preserving)
- Retrieval service tests updated to the new `RetrievalService(index_version_repository, search_strategy)` constructor signature

## [0.2.2] - 2026-09-23

### Added
- **RetrievalFilter model:** `RetrievalFilter` in `src/models/retrieval.py` consolidating `source`, `document_id`, and `document_type` into a single reusable, `extra="forbid"` filter object
- **Unified filter API:** `RetrievalQuery.filters` replaces individual filter fields

### Changed
- `RetrievalQuery` now uses `filters: RetrievalFilter | None` instead of individual `source`, `document_id`, `document_type` fields
- `VectorSearchRepository.search()` accepts `filters: RetrievalFilter | None` and applies every filter from the object in SQL via a `documents` join
- `RetrievalService.search()` forwards `request.filters` to the repository
- Filter tests construct `RetrievalFilter(source=..., document_id=..., document_type=...)` instead of passing individual fields

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
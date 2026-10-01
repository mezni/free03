# Acceptance Criteria

## Document Ingestion

- A new document can be discovered.
- The document is loaded successfully.
- The document is parsed.
- Metadata is extracted.
- The document is chunked.
- Embeddings are generated.
- Chunks and embeddings are persisted.
- The document becomes active.

## Change Detection

- New documents are processed.
- Modified documents are reprocessed.
- Unchanged documents are skipped.
- Processing history records the operation.

## Retrieval

- Queries search only the ACTIVE index.
- Vector retrieval works.
- Keyword retrieval works.
- Hybrid retrieval works.
- Metadata filters work.
- Candidate retrieval and final top-k are independent.

## Generation

- The LLM receives retrieved context.
- The LLM is instructed to use only supplied sources.
- Retrieved documents are treated as untrusted data.
- Answers contain citations when supporting sources exist.
- Unsupported information is not intentionally invented.

## Reindexing

- A BUILDING index can be created.
- Documents can be indexed into the BUILDING index.
- The BUILDING index is validated.
- A valid index can become ACTIVE.
- The previous ACTIVE index becomes RETIRED.
- A failed reindex leaves the previous ACTIVE index available.

## API

- `/health` reports liveness.
- `/health/ready` verifies database readiness.
- `/rag/query` accepts a valid question.
- Invalid requests return validation errors.
- Protected endpoints require authentication.
- Errors contain a request ID.
- Internal implementation details are not exposed.

## Reliability

- Transient provider failures can be retried.
- Retry uses backoff.
- Circuit breaker prevents repeated calls to an unavailable provider.
- Request timeouts are enforced.

## Observability

- Requests have correlation IDs.
- Retrieval and generation operations are measured.
- LLM usage is tracked.
- Audit events can be persisted.

## Evaluation

- Retrieval metrics can be calculated.
- RAG answer metrics can be calculated.
- Quality gates can fail CI when configured thresholds are not met.
# Troubleshooting

## Common Issues

### 1. Database Connection Failures

**Symptoms**: `/health/ready` returns 503, API startup fails

**Checks**:
- Verify PostgreSQL is running: `docker compose ps`
- Check `DATABASE_URL` in `.env`
- Ensure `POSTGRES` service is healthy in docker compose

**Resolution**:
- Restart PostgreSQL: `docker compose restart db`
- Verify network connectivity: `pg_isready -h localhost`
- Check environment variables are correctly set

### 2. Embedding Dimension Mismatch

**Symptoms**: Retrieval queries fail, "dimension mismatch" errors

**Checks**:
- Verify embedding provider configuration
- Check that all chunks use the same embedding dimension
- Inspect `embeddings` table for consistent dimensions

**Resolution**:
- Reindex documents after changing embedding provider
- Use `uv run python -m src.cli.evaluate` to diagnose
- Ensure `pgvector` extension is enabled

### 3. Reranker Not Functioning

**Symptoms**: Results appear in arbitrary order, reranking has no effect

**Checks**:
- Verify `reranking.enabled` setting in config
- Check that `reranking.candidate_k` >= `top_k`
- Verify SimpleReranker is properly wired

**Resolution**:
- Set `reranking.enabled: true` in YAML config
- Ensure `candidate_k` uses `max(top_k, candidate_k)` guard
- Check `SimpleReranker` implementation

### 4. Index Version Leakage

**Symptoms**: Retrieved chunks include retired/FAILED index versions

**Checks**:
- Query `index_versions` table to verify state transitions
- Verify `VectorSearchRepository.search` uses `index_version_id` filter
- Check that `SearchStrategy.search` takes index version explicitly

**Resolution**:
- This was fixed in ADR-003: ensure all search queries filter by current ACTIVE index version
- Run `alembic upgrade head` to apply schema fixes
- Verify `uq_chunks_document_version_index` constraint is enforced

### 5. Failed Reindex Leaves Index Unavailable

**Symptoms**: After a failed reindex, the knowledge base is unavailable

**Expected Behavior**: A failed reindex must NOT make the currently active knowledge base unavailable (per product principle)

**Checks**:
- Verify `index_versions` table: previous ACTIVE should still be ACTIVE
- Check that `Activate new index` step only proceeds on validation success
- Inspect migration `e71285cbb8e1_add_index_versions.py` for version lifecycle logic

**Resolution**:
- If reindex fails, the BUILDING index is discarded
- The previous ACTIVE index remains serving queries
- Investigate validation failures in `IndexValidationService`
- Check `ingestion_runs` for error details

### 7. API Authentication Failures

**Symptoms**: `/rag/query` returns 401/403

**Checks**:
- Verify `X-API-Key` header is sent
- Check that `API_KEY` in `.env` matches what the client uses
- Verify security middleware is properly configured

**Resolution**:
- Include `X-API-Key: <api-key>` header in all API requests
- Ensure `.env` `API_KEY` is set and not expired
- Check `src/api/security.py` for auth logic

### 8. Performance Degradation

**Symptoms**: Queries taking increasingly longer

**Checks**:
- Monitor query latency via `/metrics` endpoint
- Check pgvector index performance
- Verify `top_k` is not unnecessarily large
- Check `candidate_k` is optimized for reranking

**Resolution**:
- Tune `reranking.candidate_k` (use `max(top_k, candidate_k)`)
- Optimize pgvector index (IVFFlat, HNSW)
- Review and prune old ingestion runs
- Check for unbounded query growth

## When to Escalate

- All health checks failing – restart all containers
- Database consistently unreachable – check PostgreSQL logs
- Embedding provider consistently timing out – verify API keys and rate limits
- LLM provider consistently failing – verify OpenRouter API key and quotas
- Repeated reindex failures – investigate document-level errors
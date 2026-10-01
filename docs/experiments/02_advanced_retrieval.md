# Experiment 02 — Advanced Retrieval

## What was built

The retrieval pipeline now runs five independently testable stages, each
optional and each injectable:

```
query
  ↓
query analysis        SimpleQueryAnalyzer
  ↓
hybrid retrieval      RetrievalService → HybridSearchStrategy (RRF)
  ↓
reranking             SimpleReranker
  ↓
context-window        ContextWindowService
  ↓
context selection     SimpleContextSelector
```

Configuration lives in `config/advanced_retrieval.yaml` and is loaded into
`Settings.advanced_retrieval`:

| Setting | Default | Meaning |
|---|---|---|
| `query.expansion_enabled` | `false` | reserved; expansion is not executed yet |
| `query.max_queries` | `3` | reserved |
| `context.window_enabled` | `true` | pull neighbouring chunks |
| `context.window_size` | `1` | chunks either side |
| `context.max_chunks` | `8` | final context budget |
| `reranking.enabled` | `true` | rerank the candidate pool |
| `reranking.candidate_k` | `20` | pool size, never narrower than caller's `top_k` |

Two tuning guards are worth stating explicitly, because both are tested:

- `candidate_k` uses `max(top_k, candidate_k)`. Reranking can only reorder
  what retrieval returned, so the pool must be at least as wide as what the
  caller asked for.
- `max_chunks` uses `max(top_k, max_chunks)`. A context cap below the caller's
  `top_k` would silently drop results they asked for.

## Metrics

Four new metrics distinguish *ranking* quality from *context* quality:

- `recall_at_k` / `precision_at_k` / `mrr` / `ndcg_at_k` — measure the ranked
  list.
- `context_recall` / `context_precision` — measure what actually reached the
  prompt.

They are computed over separate inputs. `RetrievalMetricsService.evaluate()`
takes an optional `context_chunk_ids`; when omitted both context metrics stay
`None` rather than being inferred from the ranked list, because inferring them
would make the numbers meaningless.

## Measured results

Corpus: 9 documents (one long document whose answer sits in a middle chunk,
plus 8 vocabulary-sharing distractors), 1 evaluation case, `k=5`.

| Configuration | R@5 | P@5 | ctx recall | ctx precision |
|---|---|---|---|---|
| baseline (hybrid only) | 1.000 | 0.200 | 1.000 | 0.125 |
| + rerank | 1.000 | 0.200 | 1.000 | 0.200 |
| + window | 1.000 | 0.200 | 1.000 | 0.125 |
| advanced (rerank + window) | 1.000 | 0.200 | 1.000 | 0.167 |

Reproduce with:

```bash
uv run python -m src.cli.evaluate --dataset <dataset.yaml> --k 5
```

### These numbers do not support a quality claim

The four configurations are indistinguishable. The cause is the embedding
provider, not the pipeline.

`LocalEmbeddingProvider` (`src/providers/embeddings/local.py`) is a
deterministic SHA-256 hash stub:

```python
digest = hashlib.sha256(f"{index}:{text}".encode()).digest()
```

It encodes no semantic content. In 8 dimensions, cosine similarity between any
two unrelated texts concentrates near zero, so vector search returns results in
effectively arbitrary order and the reranker has no signal to reorder. Recall is
1.000 everywhere simply because there is only one evaluation case and 11
retrievable chunks, so `top_k=5` cannot miss it.

Two smaller observations that *are* real:

- Reranking raised context precision from 0.125 to 0.200 in isolation. With
  arbitrary scores, putting the labelled chunk first is what changed. Treat
  this as noise.
- Window expansion pulled in chunk index 1 alongside the answer chunk, which is
  the behaviour it is supposed to have, but the added chunk is not in the
  relevant set, so context precision fell from 0.200 to 0.167 when combined
  with reranking. This is the expected padding trade-off, not a regression.

### What is needed for a real comparison

1. A semantic embedding provider (e.g. a sentence-transformers model) so that
   scores actually correlate with relevance.
2. An evaluation dataset large enough to be discriminating — dozens of cases
   with multiple relevant chunks each, so that `top_k` can miss something.
3. A cross-encoder or LLM reranker; `SimpleReranker` preserves the incoming
   order and so cannot change ranking quality at all.

Until then, the advanced retrieval stages are verified correct by unit and
integration tests, but not demonstrated to improve retrieval quality.

## Verification status

- `uv run ruff check .` — clean
- `uv run ruff format --check .` — clean
- `uv run mypy src` — clean
- `uv run pytest` — 450 passed
- `alembic downgrade base && alembic upgrade head` — round-trips

## Bugs found and fixed during this phase

Three defects surfaced while wiring and validating the pipeline. All are fixed
and covered by tests.

1. **Version isolation was absent from search.**
   `VectorSearchRepository.search` and `KeywordSearchRepository.search` took no
   `index_version_id` at all, so retired index versions leaked into results.
   `ChunkDB.index_version_id` is now a required argument and a `WHERE` clause in
   both repositories, and `SearchStrategy.search` takes the version explicitly.
   This was the invariant the whole phase was meant to protect, and it was not
   actually enforced anywhere.

2. **`HybridSearchStrategy` broke the query path.**
   `RetrievalService` reached for `self.search_strategy.embedding_provider`,
   which only `VectorSearchStrategy` has. With the container wiring hybrid
   search, every request raised `AttributeError`. `RetrievalService` now holds
   its own `embedding_provider` dependency.

3. **Dead code masking type errors.** `IngestionPersistenceService` was
   unreferenced and predated the `index_version_id` requirement on chunks. It
   was deleted rather than patched; `IndexingService` superseded it.
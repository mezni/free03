# Product Requirements Document

## Product Vision

RAG System is an enterprise knowledge retrieval and question-answering platform that allows applications to ingest organizational documents and answer questions using those documents with source citations.

## Target Users

### Knowledge Administrator

- Ingests documents into the knowledge base
- Reindexes the knowledge base when documents change
- Monitors ingestion/index health and status
- Manages document versions and metadata

### Application Developer

- Integrates the /rag/query endpoint into applications
- Uses citations in their application logic
- Monitors API health and error rates
- Configures retrieval parameters (top_k, reranking, etc.)

### End User

- Asks questions about the organization's knowledge
- Receives answers grounded in indexed documents
- Gets citations to supporting sources

## Business Goals

- Reduce the effort required to locate and understand information in organizational documents
- Provide programmatic access to organizational knowledge
- Ensure answers are grounded in source documents with citations

## Functional Requirements

### Document Ingestion

- Discover new and modified documents
- Load documents from the filesystem
- Parse document formats (Markdown, Text)
- Clean and normalize document text
- Extract metadata from documents
- Chunk content into manageable units
- Generate embeddings for chunks
- Persist chunks and embeddings to PostgreSQL
- Mark documents as ACTIVE when indexing completes

### Change Detection

- Track document changes (new, modified, unchanged)
- Reprocess modified documents
- Skip unchanged documents during reindexing
- Record processing history in ingestion_runs and document_processing tables

### Retrieval

- Query only the ACTIVE index
- Vector search with pgvector cosine distance
- Keyword search with metadata filtering
- Hybrid search (vector + keyword)
- Reranking of candidate results
- Context window expansion
- Context selection (top-k from reranked pool)

### Generation

- Prompt construction with retrieved context
- LLM provider integration (OpenRouter)
- Citation extraction from generated answers
- Grounding validation (ensure answers are supported by sources)
- RAG response format with answer, citations, and metadata

### Index Versioning

- Create BUILDING index for reindexing
- Process documents into BUILDING index
- Validate BUILDING index (structural checks, embedding dimensions, duplicates)
- Activate valid BUILDING index as new ACTIVE index
- Retire previous ACTIVE index to RETIRED state
- Failed reindex leaves previous ACTIVE index available

### API Endpoints

- GET /health – liveness probe
- GET /health/ready – database readiness probe
- POST /rag/query – submit a question and retrieve an answer

### Evaluation

- Calculate retrieval metrics (recall@k, precision@k, MRR, nDCG@k)
- Calculate RAG answer metrics (grounding, citation quality)
- Quality gates that can fail CI when thresholds are not met
- Persist evaluation datasets and results

### Observability

- Correlation IDs for request tracing
- Measure retrieval and generation operation latency
- Track LLM token usage
- Persist audit events for compliance

### Reliability

- Retry transient provider failures with backoff
- Circuit breaker prevents repeated calls to unavailable providers
- Enforce request timeouts
- Errors contain request IDs; internal details are not exposed

## Non-Functional Requirements

- Python 3.12+ compatibility
- FastAPI for API layer
- PostgreSQL with pgvector for persistence
- OpenRouter as LLM provider
- Alembic for database migrations
- Docker for deployment
- ruff for linting
- mypy for type checking
- pytest for testing

## API Contract

### Health

```
GET /health
Response: {"status": "ok"}
```

### Readiness

```
GET /health/ready
Purpose: Verify that the application can reach PostgreSQL
```

### RAG Query

```
POST /rag/query
Headers: X-API-Key: <api-key>, Content-Type: application/json
Request: {"query": "What is the billing dispute policy?", "top_k": 5}
Response: {
  "query": "What is the billing dispute policy?",
  "answer": "...",
  "citations": [
    {"citation_id": "SOURCE-1", "document_id": "...", "chunk_id": "...", "chunk_index": 0}
  ],
  "model_name": "openai/gpt-oss-20b:free",
  "retrieved_count": 3
}
```

### Error Contract

```
{
  "error": {
    "code": "provider_timeout",
    "message": "The generation provider timed out.",
    "request_id": "..."
  }
}
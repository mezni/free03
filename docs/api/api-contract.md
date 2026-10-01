# API Product Contract

## Health

GET /health

Response:

{
  "status": "ok"
}

## Readiness

GET /health/ready

Purpose:

Verify that the application can reach PostgreSQL.

## RAG Query

POST /rag/query
X-API-Key: <api-key>
Content-Type: application/json

Request:

{
  "query": "What is the billing dispute policy?",
  "top_k": 5
}

Response:

{
  "query": "What is the billing dispute policy?",
  "answer": "...",
  "citations": [
    {
      "citation_id": "SOURCE-1",
      "document_id": "...",
      "chunk_id": "...",
      "chunk_index": 0
    }
  ],
  "model_name": "openai/gpt-oss-20b:free",
  "retrieved_count": 3
}

## Error Contract

{
  "error": {
    "code": "provider_timeout",
    "message": "The generation provider timed out.",
    "request_id": "..."
  }
}
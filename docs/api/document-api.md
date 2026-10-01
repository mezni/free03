# Document API

## Authentication

All document management endpoints require API key authentication via the `X-API-Key` header.

- **Public endpoints**: `GET /health`, `GET /health/ready`
- **Protected endpoints**: All `/documents/*` endpoints require valid API key

## Endpoints

### List Documents

```
GET /documents
Headers: X-API-Key: <api-key>
Query Parameters:
  - source: optional filter by source (e.g., "filesystem")
  - status: optional filter by status (e.g., "ACTIVE")
  - limit: default 50, max 100
  - offset: default 0
Response:
{
  "items": [
    {
      "id": "uuid",
      "source": "string",
      "source_uri": "string",
      "title": "string | null",
      "document_type": "string | null",
      "status": "string",
      "created_at": "ISO datetime | null",
      "updated_at": "ISO datetime | null"
    }
  ],
  "total": 0
}
```

### Get Document

```
GET /documents/{document_id}
Headers: X-API-Key: <api-key>
Path Parameters:
  - document_id: UUID
Response:
{
  "id": "uuid",
  "source": "string",
  "source_uri": "string",
  "title": "string | null",
  "document_type": "string | null",
  "content_hash": "string (sha256)",
  "status": "string",
  "created_at": "ISO datetime | null",
  "updated_at": "ISO datetime | null"
}
```

Error response (404):
```json
{
  "error": {
    "code": "document_not_found",
    "message": "The requested document was not found.",
    "request_id": "..."
  }
}
```

### Ingest Document

```
POST /documents/ingest
Headers: X-API-Key: <api-key>
Content-Type: application/json
Request:
{
  "path": "data/raw/billing"
}
Response:
{
  "run_id": "uuid",
  "discovered_count": 3,
  "processed_count": 2,
  "skipped_count": 1,
  "failed_count": 0,
  "document_ids": ["uuid", "uuid"]
}
```

### Delete Document

```
DELETE /documents/{document_id}
Headers: X-API-Key: <api-key>
Path Parameters:
  - document_id: UUID
Response: 204 No Content

Error responses:
- 404 Not Found: document not found
  ```json
  {
    "error": {
      "code": "document_not_found",
      "message": "The requested document was not found.",
      "request_id": "..."
    }
  }
  ```

## Error Codes

- `document_not_found` – requested document does not exist
- `invalid_api_key` – authentication failed
- `validation_error` – request validation failed
# Deployment

## Development Environment

```bash
# Start dependencies (PostgreSQL)
docker compose up -d

# Apply database migrations
uv run alembic upgrade head

# Start the API server
uv run uvicorn src.api.app:create_app --factory --reload
```

## Production Deployment

```bash
# Use production compose file
docker compose -f docker-compose.prod.yml up -d
```

## Database Migrations

```bash
# Create a new migration
uv run alembic revision --autogenerate -m "description of changes"

# Apply pending migrations
uv run alembic upgrade head

# Rollback last migration
uv run alembic downgrade -1
```

## Health Checks

### Liveness

```
GET http://<host>:8000/health
Response: {"status": "ok"}
```

### Readiness

```
GET http://<host>:8000/health/ready
Response: 200 if PostgreSQL is reachable, 503 if not
```

## Environment Configuration

Copy `.env.example` to `.env` and configure:

- `DATABASE_URL` – PostgreSQL connection string
- `EMBEDDING_PROVIDER` – embedding service name
- `LLM_PROVIDER` – LLM service name
- `OPENROUTER_API_KEY` – OpenRouter authentication
- `API_KEY` – API key for /rag/query authentication
- `CHUNK_SIZE` – default chunking size
- `CHUNK_OVERLAP` – default chunk overlap
- `TOP_K` – default retrieval count
- `MAX_CHUNKS` – maximum context chunks

## Rolling Restarts

1. New index is built in BUILDING state
2. Validation passes
3. New index becomes ACTIVE
4. Previous ACTIVE becomes RETIRED
5. Old containers can be restarted without downtime
6. Failed reindex leaves previous ACTIVE index available
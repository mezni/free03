#!/usr/bin/env sh

set -eu

echo "Running database migrations..."

uv run --no-dev alembic upgrade head

echo "Starting API..."

exec uv run --no-dev \
    uvicorn \
    src.api.app:app \
    --host 0.0.0.0 \
    --port 8000
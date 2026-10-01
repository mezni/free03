# Operations Runbook

## Start Development Environment

docker compose up -d

## Run Migrations

uv run alembic upgrade head

## Run Tests

uv run pytest

## Lint

uv run ruff check .

## Type Check

uv run mypy src

## Start API

uv run uvicorn src.api.app:create_app --factory --reload

## Check Health

curl http://localhost:8000/health

## Check Readiness

curl http://localhost:8000/health/ready

## Run Retrieval Evaluation

uv run python -m src.cli.evaluate

## Run RAG Evaluation

uv run python -m src.cli.evaluate_rag
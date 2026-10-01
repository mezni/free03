.PHONY: up down ps logs db-shell test lint format format-check typecheck migrate ci

up:
	docker compose up -d

down:
	docker compose down

ps:
	docker compose ps

logs:
	docker compose logs -f postgres

db-shell:
	docker compose exec postgres psql -U rag -d rag_system -h localhost -p 5432

test:
	uv run pytest

lint:
	uv run ruff check .

format:
	uv run ruff format .

format-check:
	uv run ruff format --check .

typecheck:
	uv run mypy src

migrate:
	uv run alembic upgrade head

ci:
	uv run ruff check .
	uv run mypy src
	uv run pytest
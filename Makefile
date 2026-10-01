.PHONY: up down ps logs db-shell test lint format format-check typecheck \
	migrate ci prod-build prod-up prod-down prod-logs prod-ps \
	prod-health prod-ready smoke

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

prod-build:
	docker compose -f docker-compose.prod.yml build

prod-up:
	docker compose --env-file .env.production -f docker-compose.prod.yml up -d

prod-down:
	docker compose -f docker-compose.prod.yml down

prod-logs:
	docker compose -f docker-compose.prod.yml logs -f

prod-ps:
	docker compose -f docker-compose.prod.yml ps

prod-health:
	curl http://localhost:8000/health

prod-ready:
	curl http://localhost:8000/health/ready

smoke:
	./scripts/smoke_test.sh
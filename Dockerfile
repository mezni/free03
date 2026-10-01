FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

RUN useradd \
    --create-home \
    --shell /bin/bash \
    appuser

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock README.md ./

RUN uv sync --frozen --no-dev

COPY src ./src
COPY config ./config
COPY migrations ./migrations
COPY alembic.ini ./
COPY scripts ./scripts

RUN chmod +x /app/scripts/start.sh && \
    mkdir -p /app/data && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["/app/scripts/start.sh"]
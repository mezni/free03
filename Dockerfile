# Use an official lightweight Python image
FROM python:3.12-slim

# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Enable bytecode compilation and set Python unbuffered output
ENV UV_COMPILE_BYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Copy dependency definition files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv without installing the root package yet
RUN uv sync --frozen --no-install-project

# Copy source code and application files
COPY config/ ./config/
COPY src/ ./src/
COPY evals/ ./evals/
COPY app.py README.md ./

# Sync the root project into the environment
RUN uv sync --frozen

# Expose the Streamlit default port
EXPOSE 8501

# Run Streamlit UI by default
CMD ["uv", "run", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

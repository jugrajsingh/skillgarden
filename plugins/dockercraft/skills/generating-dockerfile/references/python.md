# Python Dockerfile Reference

Python-specific Dockerfile patterns using uv for dependency management.

## Dependency Manager

**uv** (preferred) - Fast, reliable Python package manager

## Entry Point Detection

| Check | CMD Generated |
|-------|---------------|
| `main.py` at root | `CMD ["python", "main.py"]` |
| `src/main.py` exists | `CMD ["python", "-m", "src.main"]` |
| `app.py` at root | `CMD ["python", "app.py"]` |
| `[project.scripts]` in pyproject.toml | `CMD ["script-name"]` |
| `__main__.py` in package | `CMD ["python", "-m", "packagename"]` |
| FastAPI + uvicorn | `CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]` |
| Flask | `CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]` |

## Dockerfile Template

```dockerfile
# syntax=docker/dockerfile:1

# =============================================================================
# Stage 1: Build dependencies
# =============================================================================
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

WORKDIR /app

# Install dependencies (cached layer)
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Copy source and install project
COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# =============================================================================
# Stage 2: Runtime (minimal image)
# =============================================================================
FROM python:3.12-slim-bookworm AS runtime

WORKDIR /app

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code
{copy_instructions}

# Set environment
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

USER appuser

EXPOSE {port}

{cmd_instruction}
```

## Copy Instructions by Structure

**For `src/` layout:**

```dockerfile
COPY --from=builder /app/src ./src
COPY --from=builder /app/pyproject.toml ./
```

**For flat layout with `main.py`:**

```dockerfile
COPY --from=builder /app/*.py ./
COPY --from=builder /app/{package_name} ./{package_name}
```

**For package with `__main__.py`:**

```dockerfile
COPY --from=builder /app/{package_name} ./{package_name}
```

## Framework-Specific Patterns

### FastAPI

```dockerfile
# Entry point for FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Or if using src/ layout
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Default port: `8000`

### Flask

```dockerfile
# Production with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]

# Or if using factory pattern
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:create_app()"]
```

Default port: `5000`

### Django

```dockerfile
# Production with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "project.wsgi:application"]
```

Default port: `8000`

### CLI Application

```dockerfile
# If [project.scripts] defines 'myapp'
ENTRYPOINT ["myapp"]
CMD ["--help"]

# Or module-based
ENTRYPOINT ["python", "-m", "mypackage"]
```

## .dockerignore Additions

Add these Python-specific exclusions:

```dockerignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.egg-info/
.eggs/
dist/
build/

# Virtual environments
.venv/
venv/
env/
.uv/

# Testing & Quality
.pytest_cache/
.mypy_cache/
.ruff_cache/
.coverage
htmlcov/
.tox/
.nox/

# Type stubs
.pyi
```

## Dependency Detection for Services

Scan `pyproject.toml` for these patterns:

| Dependency | Service Hint |
|------------|--------------|
| `asyncpg`, `psycopg2`, `psycopg` | postgres |
| `redis`, `aioredis` | redis |
| `elasticsearch`, `elastic-transport` | elasticsearch |
| `aiobotocore`, `boto3`, `botocore` | localstack |
| `celery`, `kombu` | rabbitmq |
| `pymongo`, `motor` | mongodb |
| `aiomysql`, `mysqlclient` | mysql |

## Health Check

For web applications, add health check endpoint and configure:

```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:{port}/health || exit 1
```

## Image Size Optimization

- Builder stage: ~500MB (includes uv, build tools)
- Runtime stage: ~150MB (minimal Python + deps only)

Tips:

- Use `--no-dev` to exclude dev dependencies
- Use `--frozen` to ensure reproducible builds
- Cache mount for `/root/.cache/uv` speeds rebuilds

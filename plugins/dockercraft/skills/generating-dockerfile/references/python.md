# Python Dockerfile Reference

Python-specific Dockerfile patterns using uv for dependency management.

## Dependency Manager

**uv** (preferred) - Fast, reliable Python package manager

## Base Image Selection

| Base | Uncompressed | Use Case |
|------|--------------|----------|
| `python:3.13-alpine3.23` | ~50MB | Smallest, pure-Python deps |
| `python:3.13-slim-trixie` | ~130MB | Need glibc, compiled extensions |
| `python:3.13-slim-bookworm` | ~130MB | Stable LTS (Debian 12) |

**Recommendation**: Alpine for pure-Python projects (pydantic, httpx, etc.)
Use trixie/bookworm if you need: numpy, pandas, scipy, or native extensions.

## Critical Rule: Same Base for Both Stages

**IMPORTANT**: Builder and runtime MUST use the same base image.

```dockerfile
# WRONG: Different bases = broken venv symlinks
FROM ghcr.io/astral-sh/uv:0.10-python3.13-alpine AS builder  # /usr/bin/python3
FROM python:3.13-slim-trixie AS runtime                       # /usr/local/bin/python3

# CORRECT: Same base for both stages
FROM python:3.13-alpine3.23 AS builder
COPY --from=ghcr.io/astral-sh/uv:0.10.0 /uv /bin/uv
# ...
FROM python:3.13-alpine3.23 AS runtime
```

The venv contains symlinks to Python. If bases differ, symlinks break.

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

## Dockerfile Template (Recommended)

```dockerfile
# =============================================================================
# Multi-stage build with uv
# =============================================================================
# Pattern: Copy uv binary from distroless into standard Python base
# Result: ~100MB final image (alpine) or ~180MB (slim)

# -----------------------------------------------------------------------------
# Stage 1: Build dependencies
# -----------------------------------------------------------------------------
FROM python:3.13-alpine3.23 AS builder

# Copy uv from distroless (pinned version)
COPY --from=ghcr.io/astral-sh/uv:0.10.0 /uv /bin/uv

WORKDIR /app

# Install dependencies (cached layer)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# -----------------------------------------------------------------------------
# Stage 2: Production runtime
# -----------------------------------------------------------------------------
FROM python:3.13-alpine3.23 AS runtime

WORKDIR /app

# Create non-root user (alpine syntax)
RUN addgroup -g 1000 appuser && adduser -u 1000 -G appuser -D appuser

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY --chown=appuser:appuser . .

# Set environment
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

USER appuser

{cmd_instruction}
```

## Alternative: Debian Slim (for native extensions)

```dockerfile
FROM python:3.13-slim-trixie AS builder
COPY --from=ghcr.io/astral-sh/uv:0.10.0 /uv /bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

FROM python:3.13-slim-trixie AS runtime
WORKDIR /app
RUN useradd --create-home --shell /bin/bash appuser
COPY --from=builder /app/.venv /app/.venv
COPY --chown=appuser:appuser . .
ENV PATH="/app/.venv/bin:$PATH" PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
USER appuser
{cmd_instruction}
```

## .dockerignore (CRITICAL)

**MUST include `.venv/`** - otherwise local venv overwrites builder's venv:

```dockerignore
# Virtual environments (CRITICAL: local .venv breaks builds)
.venv/
venv/
env/
.uv/

# Python bytecode
__pycache__/
*.py[cod]
*$py.class
*.egg-info/
dist/
build/

# Testing & Quality
.pytest_cache/
.mypy_cache/
.ruff_cache/
.coverage
htmlcov/

# Git and IDE
.git/
.gitignore
.idea/
.vscode/

# Docs and config
*.md
docs/
Makefile*
docker-compose*.yaml
```

## Framework-Specific Patterns

### FastAPI

```dockerfile
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Flask (Production)

```dockerfile
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
```

### Django (Production)

```dockerfile
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "project.wsgi:application"]
```

### CLI Application

```dockerfile
ENTRYPOINT ["python", "-u", "main.py"]
```

## Dependency Detection for Services

| Dependency | Service Hint |
|------------|--------------|
| `asyncpg`, `psycopg2`, `psycopg` | postgres |
| `redis`, `aioredis` | redis |
| `elasticsearch`, `elastic-transport` | elasticsearch |
| `aiobotocore`, `boto3`, `botocore` | localstack |
| `celery`, `kombu` | rabbitmq |
| `pymongo`, `motor` | mongodb |

## Health Check

```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:{port}/health')" || exit 1
```

## Image Size Reference

| Pattern | Final Size |
|---------|------------|
| Alpine + uv distroless copy | ~100MB |
| Trixie-slim + uv distroless copy | ~180MB |
| Full `uv:python` image | ~250MB |

## Common Pitfalls

| Issue | Cause | Fix |
|-------|-------|-----|
| `python: not found` | Different base images | Use same base for builder/runtime |
| Local packages in image | `.venv/` not in .dockerignore | Add `.venv/` to .dockerignore |
| Large image | Using full uv image | Copy `/uv` from distroless |
| Slow rebuilds | No layer caching | Separate `COPY pyproject.toml` from `COPY .` |

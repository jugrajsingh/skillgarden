# Multi-Language Dockerfile Reference

Strategies for containerizing projects with multiple languages (e.g., Python backend + React frontend).

## Common Scenarios

| Scenario | Recommended Approach |
|----------|---------------------|
| API + SPA Frontend | Separate containers |
| Monorepo (backend + frontend) | Separate containers OR single with nginx |
| Python + Node.js tooling | Single container (Node for build only) |
| Go + React dashboard | Single multi-stage |

## Approach 1: Separate Containers (Recommended)

Best for: Microservices, independent scaling, CI/CD flexibility

### Directory Structure

```text
project/
├── backend/
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── src/
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   └── src/
├── docker-compose.yml
└── .dockerignore
```

### docker-compose.yml

```yaml
services:
  api:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/app

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:80"
    depends_on:
      - api

  db:
    image: postgres:16-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Separate Dockerfiles

**backend/Dockerfile** - Use `./python.md` template

**frontend/Dockerfile** - Use `./nodejs.md` React/nginx template

## Approach 2: Single Container with nginx

Best for: Simple deployments, static frontend + API backend

### Dockerfile

```dockerfile
# syntax=docker/dockerfile:1

# =============================================================================
# Stage 1: Build Frontend
# =============================================================================
FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend

COPY frontend/package.json frontend/pnpm-lock.yaml ./
RUN corepack enable && pnpm install --frozen-lockfile

COPY frontend/ ./
RUN pnpm build

# =============================================================================
# Stage 2: Build Backend
# =============================================================================
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS backend-builder

WORKDIR /app

COPY backend/pyproject.toml backend/uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

COPY backend/ ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# =============================================================================
# Stage 3: Runtime with nginx
# =============================================================================
FROM python:3.12-slim-bookworm AS runtime

# Install nginx
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy Python environment
COPY --from=backend-builder /app/.venv /app/.venv
COPY --from=backend-builder /app/src ./src

# Copy frontend build
COPY --from=frontend-builder /app/frontend/dist /usr/share/nginx/html

# Copy nginx config
COPY nginx.conf /etc/nginx/nginx.conf

ENV PATH="/app/.venv/bin:$PATH"

# Supervisord or start script to run both
COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 80

CMD ["/start.sh"]
```

### start.sh

```bash
#!/bin/bash
# Start nginx in background
nginx &

# Start Python app
exec uvicorn src.main:app --host 127.0.0.1 --port 8000
```

### nginx.conf

```nginx
events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    server {
        listen 80;

        # Serve static frontend
        location / {
            root /usr/share/nginx/html;
            index index.html;
            try_files $uri $uri/ /index.html;
        }

        # Proxy API requests to backend
        location /api {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
```

## Approach 3: Go Backend + React Frontend

Best for: Go APIs with embedded static files

### Dockerfile

```dockerfile
# syntax=docker/dockerfile:1

# =============================================================================
# Stage 1: Build Frontend
# =============================================================================
FROM node:20-alpine AS frontend

WORKDIR /app/frontend

COPY frontend/package.json frontend/pnpm-lock.yaml ./
RUN corepack enable && pnpm install --frozen-lockfile

COPY frontend/ ./
RUN pnpm build

# =============================================================================
# Stage 2: Build Go with embedded frontend
# =============================================================================
FROM golang:1.22-alpine AS builder

WORKDIR /app

RUN apk add --no-cache ca-certificates

COPY go.mod go.sum ./
RUN go mod download

COPY . .

# Copy frontend build into Go embed directory
COPY --from=frontend /app/frontend/dist ./internal/web/dist

RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-w -s" -o /app/bin/server ./cmd/server

# =============================================================================
# Stage 3: Runtime
# =============================================================================
FROM scratch

COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /app/bin/server /server

USER 1000:1000

EXPOSE 8080

ENTRYPOINT ["/server"]
```

### Go embed example

```go
package web

import "embed"

//go:embed dist/*
var StaticFiles embed.FS
```

## Approach 4: Node.js for Build Tools Only

When Python project needs Node.js just for building (e.g., Tailwind, esbuild):

```dockerfile
# syntax=docker/dockerfile:1

# =============================================================================
# Stage 1: Build frontend assets with Node
# =============================================================================
FROM node:20-alpine AS assets

WORKDIR /app

COPY package.json pnpm-lock.yaml ./
RUN corepack enable && pnpm install --frozen-lockfile

COPY tailwind.config.js postcss.config.js ./
COPY src/static ./src/static
RUN pnpm build:css

# =============================================================================
# Stage 2: Python app
# =============================================================================
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

COPY . .
# Copy built assets
COPY --from=assets /app/src/static/dist ./src/static/dist

RUN uv sync --frozen --no-dev

# =============================================================================
# Stage 3: Runtime
# =============================================================================
FROM python:3.12-slim-bookworm

WORKDIR /app

RUN useradd --create-home appuser

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src ./src

ENV PATH="/app/.venv/bin:$PATH"

USER appuser

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Decision Guide

```text
Is frontend served separately (CDN, Vercel, etc.)?
├─ Yes → Backend-only Dockerfile
└─ No → Do they scale independently?
         ├─ Yes → Separate containers (docker-compose)
         └─ No → Is it a simple deployment?
                  ├─ Yes → Single container with nginx
                  └─ No → Separate containers
```

## .dockerignore for Multi-Language

```dockerignore
# Git
.git/
.gitignore

# Both languages
node_modules/
__pycache__/
*.pyc
.venv/
dist/
build/

# IDE
.idea/
.vscode/

# Environment
*.env
*.env.*
!*.env.example

# Docker
Dockerfile*
docker-compose*.yml
.dockerignore

# Testing
coverage/
.pytest_cache/
htmlcov/

# Docs
*.md
!README.md
docs/
```

## Tips

1. **Order stages by change frequency** - Put less-changing stages first
2. **Share cache mounts** - Use consistent paths for package caches
3. **Minimize cross-stage copies** - Only copy what's needed
4. **Use specific tags** - Not `latest` for reproducibility
5. **Consider build time** - Parallel builds in separate containers are faster

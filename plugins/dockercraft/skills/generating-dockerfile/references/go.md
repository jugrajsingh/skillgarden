# Go Dockerfile Reference

Go-specific Dockerfile patterns for statically compiled binaries.

## Key Advantages

- **Static binaries** - No runtime dependencies
- **Scratch/distroless images** - Minimal attack surface (~10MB)
- **Fast builds** - Go module caching

## Entry Point Detection

| Check | Binary Name |
|-------|-------------|
| `go.mod` module path | Last segment of module path |
| `cmd/` directory | Subdirectory names |
| `main.go` at root | Project directory name |

## Dockerfile Templates

### Standard Go Binary

```dockerfile
# syntax=docker/dockerfile:1

# =============================================================================
# Stage 1: Build
# =============================================================================
FROM golang:1.22-alpine AS builder

WORKDIR /app

# Install certificates for HTTPS
RUN apk add --no-cache ca-certificates

# Download dependencies (cached layer)
COPY go.mod go.sum ./
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download

# Build binary
COPY . .
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
    go build -ldflags="-w -s" -o /app/bin/{binary_name} ./cmd/{binary_name}

# =============================================================================
# Stage 2: Runtime (scratch - minimal)
# =============================================================================
FROM scratch AS runtime

# Copy CA certificates for HTTPS
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

# Copy binary
COPY --from=builder /app/bin/{binary_name} /{binary_name}

# Non-root user (numeric for scratch)
USER 1000:1000

EXPOSE {port}

ENTRYPOINT ["/{binary_name}"]
```

### Go with CGO (requires glibc)

```dockerfile
# syntax=docker/dockerfile:1

# =============================================================================
# Stage 1: Build
# =============================================================================
FROM golang:1.22-bookworm AS builder

WORKDIR /app

# Install build dependencies for CGO
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libc6-dev \
    && rm -rf /var/lib/apt/lists/*

COPY go.mod go.sum ./
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download

COPY . .
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    CGO_ENABLED=1 GOOS=linux GOARCH=amd64 \
    go build -ldflags="-w -s" -o /app/bin/{binary_name} ./cmd/{binary_name}

# =============================================================================
# Stage 2: Runtime (distroless for glibc)
# =============================================================================
FROM gcr.io/distroless/base-debian12 AS runtime

COPY --from=builder /app/bin/{binary_name} /{binary_name}

USER nonroot:nonroot

EXPOSE {port}

ENTRYPOINT ["/{binary_name}"]
```

### Go with Multiple Binaries

```dockerfile
# syntax=docker/dockerfile:1

FROM golang:1.22-alpine AS builder

WORKDIR /app

RUN apk add --no-cache ca-certificates

COPY go.mod go.sum ./
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download

COPY . .

# Build all binaries in cmd/
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    for cmd in cmd/*/; do \
        name=$(basename "$cmd"); \
        CGO_ENABLED=0 GOOS=linux go build -ldflags="-w -s" -o /app/bin/$name ./cmd/$name; \
    done

# =============================================================================
# Runtime for specific binary
# =============================================================================
FROM scratch AS api
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /app/bin/api /api
USER 1000:1000
EXPOSE 8080
ENTRYPOINT ["/api"]

FROM scratch AS worker
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /app/bin/worker /worker
USER 1000:1000
ENTRYPOINT ["/worker"]
```

## Build Flags

| Flag | Purpose |
|------|---------|
| `CGO_ENABLED=0` | Pure Go, no C dependencies |
| `GOOS=linux` | Target Linux |
| `GOARCH=amd64` | Target AMD64 (or `arm64`) |
| `-ldflags="-w -s"` | Strip debug info, smaller binary |
| `-trimpath` | Remove file paths from binary |

### Production build with version

```dockerfile
ARG VERSION=dev
RUN go build -ldflags="-w -s -X main.version=${VERSION}" -o /app/bin/myapp .
```

## .dockerignore Additions

Add these Go-specific exclusions:

```dockerignore
# Go
*.exe
*.exe~
*.dll
*.so
*.dylib
*.test
*.out

# Go workspace
go.work
go.work.sum

# Binaries
bin/
dist/

# Vendor (if not vendoring)
# vendor/

# IDE
.idea/
*.iml
```

## Dependency Detection for Services

Scan `go.mod` for:

| Module | Service Hint |
|--------|--------------|
| `github.com/lib/pq`, `github.com/jackc/pgx` | postgres |
| `github.com/go-redis/redis`, `github.com/redis/go-redis` | redis |
| `github.com/elastic/go-elasticsearch` | elasticsearch |
| `go.mongodb.org/mongo-driver` | mongodb |
| `github.com/streadway/amqp`, `github.com/rabbitmq/amqp091-go` | rabbitmq |
| `github.com/segmentio/kafka-go`, `github.com/confluentinc/confluent-kafka-go` | kafka |
| `github.com/go-sql-driver/mysql` | mysql |
| `github.com/aws/aws-sdk-go-v2` | localstack |

## Base Image Options

| Image | Size | Use Case |
|-------|------|----------|
| `scratch` | ~0MB | CGO_ENABLED=0, pure Go |
| `gcr.io/distroless/static` | ~2MB | Static binary + CA certs |
| `gcr.io/distroless/base` | ~20MB | CGO with glibc |
| `alpine` | ~8MB | Need shell/debugging |

## Framework-Specific Ports

| Framework | Default Port |
|-----------|--------------|
| Standard library | 8080 |
| Gin | 8080 |
| Echo | 8080 |
| Fiber | 3000 |
| Chi | 8080 |

## Image Size Optimization

Typical sizes:

- Build stage: ~1GB (Go toolchain + modules)
- Runtime (scratch): ~10-20MB (just binary + certs)
- Runtime (distroless): ~20-30MB
- Runtime (alpine): ~15-25MB (with shell)

Tips:

- Always use `-ldflags="-w -s"` to strip debug info
- Use `scratch` when possible (CGO_ENABLED=0)
- Cache `/go/pkg/mod` and `/root/.cache/go-build`

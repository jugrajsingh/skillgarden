---
name: optimizing
description: Analyze Docker image layers and suggest optimizations for size reduction, build speed, and caching efficiency.
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
  - Bash(docker images *)
  - Bash(docker inspect *)
  - Bash(docker history *)
---

# Optimize Docker Images

Analyze Docker image layers and apply optimizations for size and build performance.

## Analysis Steps

### 1. Check Current Image

```bash
docker images {image_name} --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
```

### 2. Analyze Layers

```bash
docker history {image_name}:{tag} --no-trunc --format "table {{.Size}}\t{{.CreatedBy}}"
```

### 3. Read Dockerfile

```text
Glob: Dockerfile, Dockerfile.*
```

Read and analyze the current Dockerfile structure.

## Optimization Checks

### Size Optimizations

| Check | Optimization |
|-------|-------------|
| Base image | Switch to alpine/slim/distroless |
| Multi-stage | Convert single-stage to multi-stage |
| Dev deps in runtime | Remove build tools from final stage |
| Package cache | Clean apt/apk cache in same RUN layer |
| Unnecessary files | Add to .dockerignore |
| Layer count | Combine related RUN commands |

### Build Speed Optimizations

| Check | Optimization |
|-------|-------------|
| Layer ordering | Move frequently changing layers last |
| Cache mounts | Add --mount=type=cache for package managers |
| Dependency caching | Copy lock files before source code |
| BuildKit features | Enable DOCKER_BUILDKIT=1 |

### Caching Optimizations

| Check | Optimization |
|-------|-------------|
| Lock file first | COPY package.json before COPY . |
| Source last | Application code copied last |
| Build cache | Use --mount=type=cache |

## Workflow

### 1. Analyze Current State

Gather image size, layer count, and Dockerfile content.

### 2. Identify Optimizations

Compare against checklist and identify applicable improvements.

### 3. Present Findings

Show before/after comparison for each optimization with estimated impact.

### 4. Ask User

Via AskUserQuestion:

- "Apply all optimizations" - Rewrite Dockerfile
- "Apply selected" - Choose which to apply
- "Report only" - No changes

### 5. Apply Changes

If requested, rewrite Dockerfile with optimizations applied.

### 6. Generate Report

Use optimization-report.md template.

## Common Optimizations

### Multi-stage Conversion

Before:

```dockerfile
FROM python:3.12
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```

After:

```dockerfile
FROM python:3.12-slim AS builder
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY . .
CMD ["python", "main.py"]
```

### Cache Mount Addition

Before:

```dockerfile
RUN pip install -r requirements.txt
```

After:

```dockerfile
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt
```

### Base Image Switch

| From | To | Savings |
|------|----|---------|
| python:3.12 | python:3.12-slim | ~700MB |
| node:20 | node:20-slim | ~600MB |
| ubuntu:22.04 | debian:bookworm-slim | ~50MB |

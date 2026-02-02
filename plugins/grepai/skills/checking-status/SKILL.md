---
name: checking-status
description: Health check all GrepAI components — Docker services, Ollama, PostgreSQL, pgvector, config, index, MCP registration, and watch daemon.
allowed-tools:
  - Read
  - Glob
  - Bash(grepai *)
  - Bash(docker *)
  - Bash(curl *)
  - Bash(ollama *)
  - Bash(claude *)
---

# GrepAI Health Check

Diagnose all GrepAI components and report status with indicators.

## Workflow

Run each check sequentially. Collect results, then print a unified report.

### 1. Docker Services

Check by image ancestry rather than hardcoded container names:

```bash
docker ps --filter ancestor=ollama/ollama --format "{{.Names}}\t{{.Status}}\t{{.Ports}}"
docker ps --filter ancestor=qdrant/qdrant --format "{{.Names}}\t{{.Status}}\t{{.Ports}}"
docker ps --filter ancestor=postgres --format "{{.Names}}\t{{.Status}}\t{{.Ports}}"
```

Record: which services are running.

### 2. Ollama Connectivity

```bash
curl -s --max-time 5 http://localhost:11434/api/tags
```

Record: reachable? Parse response for available models.

### 3. Ollama Embedding Models

From the /api/tags response, list models that are embedding models:

- mxbai-embed-large
- nomic-embed-text
- bge-m3
- nomic-embed-text-v2-moe

Record: which embedding models are pulled.

### 4. PostgreSQL Connectivity

Check if a postgres container is running (from step 1). If so, get the container name and check:

```bash
docker exec {POSTGRES_CONTAINER} pg_isready -U grepai
```

Skip if config shows GOB or qdrant backend and no postgres container is running. Record: accepting connections?

### 5. pgvector Extension

```bash
docker exec {POSTGRES_CONTAINER} psql -U grepai -d grepai -tAc "SELECT extname FROM pg_extension WHERE extname='vector'"
```

Skip if config shows GOB or qdrant backend. Record: vector extension installed?

### 6. Qdrant Connectivity

Check Qdrant REST API on port **6333** (not 6334, which is gRPC):

```bash
curl -s --max-time 5 http://localhost:6333/collections
```

Skip if config does not use qdrant backend and no qdrant container is running. Record: reachable? Collection count.

### 7. grepai Config

```text
Read: .grepai/config.yaml
```

If missing, report not initialized. Otherwise extract and report:

- Provider + model
- Storage backend
- Endpoint URL

### 8. grepai Index Status

```bash
grepai status
```

Record: indexed files, chunks, last updated.

### 9. MCP Registration

```bash
claude mcp list
```

Or read `~/.claude/mcp.json` and `./.claude/mcp.json`. Record: grepai MCP server registered?

### 10. Watch Daemon

```bash
grepai watch --status
```

Record: running or not.

### 11. Workspace Config

```bash
grepai workspace list
```

If workspaces exist, get details for each:

```bash
grepai workspace show {NAME}
```

Optionally also read `~/.grepai/workspace.yaml` for additional detail.

Record: configured workspaces, backend type, project count per workspace. Skip if no workspaces configured.

### 12. Workspace Status & Watcher

```bash
grepai workspace status {NAME}
```

And check workspace watcher:

```bash
grepai watch --workspace {NAME} --status
```

Record: per-workspace indexing health and watcher state. Skip if no workspaces configured.

## Report Format

Print unified status report:

```text
============================================================================
GrepAI Health Check
============================================================================

Infrastructure:
  {S} Docker           ollama: {STATUS}
  {S} Ollama           http://localhost:11434 — {STATUS}
  {S} Models           {MODEL_LIST} (or "none pulled")
  {S} PostgreSQL       {STATUS} (only if postgres backend, otherwise "skipped")
  {S} pgvector         {STATUS} (only if postgres backend, otherwise "skipped")
  {S} Qdrant           http://localhost:6333 — {STATUS} (only if qdrant backend, otherwise "skipped")

Configuration:
  {S} Config           .grepai/config.yaml — {PROVIDER}/{MODEL}
  {S} Storage          {BACKEND}

Index:
  {S} Files indexed    {COUNT}
  {S} Chunks           {COUNT}
  {S} Last updated     {TIMESTAMP}

Integration:
  {S} MCP server       {SCOPE} — {STATUS}
  {S} Watch daemon     {STATUS}

Workspaces: (only if workspaces configured)
  {S} {WORKSPACE_1}   backend: {TYPE}, {PROJECT_COUNT} projects — {STATUS}
     Watcher: {RUNNING|STOPPED}

============================================================================
```

Where {S} is one of: OK for healthy, FAIL for failed/missing, WARN for degraded/warning.

## Troubleshooting Hints

After the report, if any component shows FAIL, print targeted fix suggestions:

| Component | Fix |
|-----------|-----|
| Docker not running | `docker compose up -d` or start Docker Desktop |
| Ollama unreachable | Start ollama container then wait 5s |
| No embedding models | `docker exec {OLLAMA_CONTAINER} ollama pull nomic-embed-text` |
| PostgreSQL down | Start postgres container |
| pgvector missing | Extensions auto-install on first grepai index |
| No config | Run `/grepai:init` to initialize |
| No index | Run `grepai index` to build initial index |
| MCP not registered | `claude mcp add grepai -- grepai mcp-serve` |
| Watch not running | `grepai watch --background` |
| Qdrant unreachable | Start qdrant container then wait 5s |
| Workspace watcher stopped | `grepai watch --workspace {NAME} --background` |
| Workspace issues | Run `/grepai:workspace:status {NAME}` for details |

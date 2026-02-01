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

Diagnose all GrepAI components and report status with ✓/✗ indicators.

## Workflow

Run each check sequentially. Collect results, then print a unified report.

### 1. Docker Services

```bash
docker ps --filter name=ollama --filter name=grepai-postgres --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

Record: ollama running? grepai-postgres running?

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

```bash
docker exec grepai-postgres pg_isready -U grepai
```

Skip if config shows GOB backend. Record: accepting connections?

### 5. pgvector Extension

```bash
docker exec grepai-postgres psql -U grepai -d grepai -tAc "SELECT extname FROM pg_extension WHERE extname='vector'"
```

Skip if config shows GOB backend. Record: vector extension installed?

### 6. grepai Config

```text
Read: .grepai/config.yaml
```

If missing, report not initialized. Otherwise extract and report:

- Provider + model
- Storage backend
- Endpoint URL

### 7. grepai Index Status

```bash
grepai status
```

Record: indexed files, chunks, last updated.

### 8. MCP Registration

```bash
claude mcp list
```

Or read `~/.claude/mcp.json` and `./.claude/mcp.json`. Record: grepai MCP server registered?

### 9. Watch Daemon

```bash
grepai watch --status
```

Record: running or not.

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
  {S} PostgreSQL       {STATUS} (only if postgres backend, otherwise "skipped — GOB")
  {S} pgvector         {STATUS} (only if postgres backend, otherwise "skipped — GOB")

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

============================================================================
```

Where {S} is ✓ for healthy, ✗ for failed/missing, △ for degraded/warning.

## Troubleshooting Hints

After the report, if any component shows ✗, print targeted fix suggestions:

| Component | Fix |
|-----------|-----|
| Docker not running | `docker compose up -d` or start Docker Desktop |
| Ollama unreachable | `docker start ollama` then wait 5s |
| No embedding models | `docker exec ollama ollama pull nomic-embed-text` |
| PostgreSQL down | `docker start grepai-postgres` |
| pgvector missing | Extensions auto-install on first grepai index |
| No config | Run `/grepai:init` to initialize |
| No index | Run `grepai index` to build initial index |
| MCP not registered | `claude mcp add grepai -- grepai mcp-serve` |
| Watch not running | `grepai watch --background` |

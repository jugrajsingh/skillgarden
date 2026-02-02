---
name: setting-up
description: Full guided setup of GrepAI semantic search — prerequisites, Docker, embedding provider/model, storage backend, MCP registration, and indexing.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash(docker *)
  - Bash(grepai *)
  - Bash(ollama *)
  - Bash(curl *)
  - Bash(which *)
  - Bash(claude *)
  - Write
  - AskUserQuestion
  - Skill
---

# GrepAI Full Setup

Guided orchestrator for GrepAI semantic code search. Walks through prerequisites, infrastructure, embedding config, storage, MCP integration, and indexing.

## Step 1: Prerequisites Check

### grepai CLI

```bash
which grepai
```

If missing, show install instructions:

```text
Install grepai:

  macOS/Linux:
    brew install grepai/tap/grepai

  Or via curl:
    curl -fsSL https://get.grepai.dev | sh

  Windows (PowerShell):
    irm https://get.grepai.dev/install.ps1 | iex
```

Stop and ask user to install before continuing.

### Docker

```bash
which docker
```

If missing, instruct to install Docker Desktop or Docker Engine and stop.

## Step 2: Storage Backend Selection

Present via AskUserQuestion:

```text
Which storage backend?

○ GOB (local file) — simple, zero config, single-project only (Recommended)
○ PostgreSQL + pgvector — scalable, team-ready, supports workspaces
○ Qdrant — lightweight vector DB, supports workspaces
```

If **GOB**: default storage, no extra config needed. Index stored in `.grepai/index.gob`.

If **PostgreSQL**: note the DSN for later:

```text
DSN: postgres://grepai:grepai@localhost:5432/grepai
```

**Known issue:** PostgreSQL + pgvector has a UTF-8 encoding bug where files
containing Unicode box-drawing characters (e.g. U+2550 ═) fail to index. GOB
does not have this limitation.

If **Qdrant**: note the endpoint for later:

```text
Endpoint: http://localhost:6334
```

## Step 3: Docker Compose Setup

Select the template based on storage choice:

- GOB → `${CLAUDE_PLUGIN_ROOT}/templates/docker-compose-ollama.yml`
- PostgreSQL → `${CLAUDE_PLUGIN_ROOT}/templates/docker-compose-postgres.yml`
- Qdrant → `${CLAUDE_PLUGIN_ROOT}/templates/docker-compose-qdrant.yml`

Read the selected template.

Present via AskUserQuestion:

```text
Where should docker-compose.yml be placed?

○ Project root (Recommended) — writes to $CLAUDE_PROJECT_DIR/docker-compose.yml
○ Custom path — you specify the location
```

Write the template to the chosen path.

If file already exists, warn and ask whether to overwrite or skip.

Then ask:

```text
Start Docker services now?

○ Yes, start services (Recommended) — runs docker compose up -d
○ No, I'll start later
```

If yes:

```bash
docker compose -f {COMPOSE_PATH} up -d
```

Verify with:

```bash
docker compose -f {COMPOSE_PATH} ps
```

## Step 4: Embedding Provider Selection

Present via AskUserQuestion:

```text
Which embedding provider?

○ Ollama — local, private, free, works offline (Recommended)
○ OpenAI — cloud, high quality, costs ~$0.01-$6.50 per full index
```

If **OpenAI**: inform about API key setup:

```text
Set your OpenAI API key:
  export OPENAI_API_KEY="sk-..."

Cost estimates per full index:
  text-embedding-3-small  ~$0.01-$0.10 (small-medium repos)
  text-embedding-3-large  ~$0.05-$6.50 (depends on repo size)
```

If **Ollama**: proceed to model selection.

## Step 5: Embedding Model Selection

Present via AskUserQuestion based on chosen provider.

**For Ollama:**

```text
Which embedding model?

○ nomic-embed-text — 768 dims, 274MB, fast general use (Recommended)
○ mxbai-embed-large — 1024 dims, 670MB, highest accuracy
○ bge-m3 — 1024 dims, 1.2GB, multilingual
○ nomic-embed-text-v2-moe — 768 dims, 500MB, multilingual MoE
```

**For OpenAI:**

```text
Which embedding model?

○ text-embedding-3-small — 1536 dims, $0.00002/1K tokens (Recommended)
○ text-embedding-3-large — 3072 dims, $0.00013/1K tokens
```

Then confirm before downloading (Ollama only):

```text
Pull embedding model now? This downloads {SIZE} to the Ollama container.

○ Yes, pull now (Recommended)
○ No, I'll pull later
```

If yes:

```bash
docker exec ollama ollama pull {MODEL}
```

## Step 6: Initialize grepai

Delegate to the initializing skill with collected choices:

Invoke the `grepai:initializing` skill and follow it exactly.

Pass context: chosen provider, model, storage backend, DSN if postgres, endpoint if qdrant.

## Step 7: MCP Registration

Present via AskUserQuestion:

```text
Where should grepai MCP server be registered?

○ Global (~/.claude/mcp.json) — available in all projects (Recommended)
○ Project (./.claude/mcp.json) — this project only
```

Register:

```bash
claude mcp add grepai -- grepai mcp-serve
```

For project-scope, add `--scope project` flag. For global, add `--scope global` flag.

## Step 8: Official Skills Plugin

Inform user about the official grepai-skills plugin:

```text
The official grepai-skills plugin provides 27 reference skills for advanced
configuration tuning, troubleshooting, and workflow optimization.

Install via Claude Code plugin marketplace:
  /plugin marketplace add yoanbernabeu/grepai-skills
  /plugin install grepai-complete@grepai-skills

Note: These are reference skills (no /commands). The grepai MCP tools
(grepai_search, grepai_trace_*) handle search and trace natively.
```

## Step 9: Start Indexing

Present via AskUserQuestion:

```text
Start grepai watch daemon now? This monitors file changes and updates the index.

○ Yes, start in background (Recommended)
○ No, I'll start later
```

If yes:

```bash
grepai watch --background
```

## Final Summary

Print configuration summary:

```text
============================================================================
GrepAI Setup Complete
============================================================================

Infrastructure:
  ✓ Docker Compose      {COMPOSE_PATH}
  ✓ Ollama              http://localhost:11434
  ✓ PostgreSQL/pgvector  localhost:5432 (only if postgres backend)
  ✓ Qdrant              localhost:6333/6334 (only if qdrant backend)

Embedding:
  ✓ Provider   {PROVIDER}
  ✓ Model      {MODEL}
  ✓ Dimensions {DIMS}

Storage:
  ✓ Backend    {BACKEND}

Integration:
  ✓ MCP server registered ({SCOPE})
  ✓ Config     .grepai/config.yaml

Commands:
  grepai status              # Check index health
  grepai watch --background  # Start file watcher
  grepai index               # Full re-index
  /grepai:status             # Health check all components
============================================================================
```

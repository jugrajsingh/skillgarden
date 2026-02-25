# Infrastructure Setup — Storage, Docker, Embedding

## Storage Backend Selection

Present via AskUserQuestion:

```text
Which storage backend?

○ GOB (local file) — simple, zero config, single-project only (Recommended)
○ PostgreSQL + pgvector — scalable, team-ready, supports workspaces
○ Qdrant — lightweight vector DB, supports workspaces
```

If **GOB**: default storage, no extra config needed. Index stored in `.grepai/index.gob`.

**Note:** If the user plans to use workspace mode (cross-project search) later, they should pick PostgreSQL or Qdrant for the workspace backend. GOB is fine for the per-project local config — the workspace has its own separate store config.

If **PostgreSQL**: note the DSN for later:

```text
DSN: postgres://grepai:grepai@localhost:5432/grepai
```

If **Qdrant**: note the endpoint for later:

```text
REST API: http://localhost:6333
gRPC:     http://localhost:6334
```

## Docker Compose Setup

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

Write the template to the chosen path. If file already exists, warn and ask whether to overwrite or skip.

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

## Embedding Provider Selection

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

## Embedding Model Selection

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

## Final Summary Template

```text
============================================================================
GrepAI Setup Complete
============================================================================

Infrastructure:
  Docker Compose      {COMPOSE_PATH}
  Ollama              http://localhost:11434
  PostgreSQL/pgvector  localhost:5432 (only if postgres backend)
  Qdrant              localhost:6333/6334 (only if qdrant backend)

Embedding:
  Provider   {PROVIDER}
  Model      {MODEL}
  Dimensions {DIMS}

Storage:
  Backend    {BACKEND}

Integration:
  MCP server registered ({SCOPE})
  Config     .grepai/config.yaml

Workspace: {NAME} (only if workspace mode)
  CLAUDE.md workspace guidance added
  Watcher: grepai watch --workspace {NAME} --background

Commands:
  grepai status              # Check index health
  grepai watch --background  # Start file watcher (single project)
  grepai watch --workspace {NAME} --background  # Workspace watcher
  grepai index               # Full re-index
  /grepai:status             # Health check all components
============================================================================
```

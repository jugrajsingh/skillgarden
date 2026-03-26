# Health Check Report Format and Troubleshooting

## Report Template

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

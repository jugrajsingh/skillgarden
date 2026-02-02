---
name: initializing
description: Initialize grepai in a project — run grepai init, configure provider/model/storage in .grepai/config.yaml, and update .gitignore.
allowed-tools:
  - Read
  - Glob
  - Bash(grepai *)
  - Write
  - AskUserQuestion
---

# GrepAI Project Initialization

Initialize grepai config for the current project with the chosen embedding provider, model, and storage backend.

## Context

This skill expects context from the `grepai:setting-up` skill:

- **provider**: ollama or openai
- **model**: embedding model name
- **backend**: postgres, qdrant, or gob
- **dsn**: PostgreSQL connection string (if postgres)
- **qdrant_endpoint**: Qdrant endpoint (if qdrant)

If invoked standalone (via /grepai:init), ask for these values via AskUserQuestion.

## Workflow

### 0. Project Scope Selection

When invoked standalone (not from setting-up skill), ask via AskUserQuestion:

```text
Project scope?

○ Single project — index this project only (Recommended)
○ Workspace — cross-project search (requires PostgreSQL or Qdrant)
```

**If workspace:**

1. Ask for workspace name (suggest based on parent directory name)
2. Check if workspace exists:

   ```bash
   grepai workspace list
   ```

3. If new workspace: invoke the `grepai:workspace-managing` skill with operation=create, then return here
4. If existing workspace: add current project:

   ```bash
   grepai workspace add {NAME} .
   ```

5. Still run steps 1-5 below for per-project settings (chunking, ignore patterns)
6. In the summary (step 6), note workspace membership

**If single project:** continue with step 1.

### 1. Check Existing Config

```text
Glob: .grepai/config.yaml
```

If `.grepai/` exists, warn:

```text
△ Existing .grepai/config.yaml found. Reinitializing will overwrite it.
```

Ask via AskUserQuestion:

```text
Existing grepai config found. What to do?

○ Overwrite — reinitialize with new settings (Recommended)
○ Cancel — keep existing config
```

If cancel, stop.

### 2. Run grepai init

```bash
grepai init
```

This creates `.grepai/config.yaml` with defaults.

### 3. Read Generated Config

```text
Read: .grepai/config.yaml
```

### 4. Write Configured Values

Overwrite `.grepai/config.yaml` with the chosen settings.

**For Ollama + GOB (most common):**

```yaml
embedder:
  provider: ollama
  model: {MODEL}
  endpoint: http://localhost:11434
  dimensions: {DIMS}
store:
  backend: gob
chunking:
  max_tokens: 512
  overlap: 50
trace:
  enabled: true
```

**For OpenAI + GOB:**

```yaml
embedder:
  provider: openai
  model: {MODEL}
  dimensions: {DIMS}
store:
  backend: gob
chunking:
  max_tokens: 512
  overlap: 50
trace:
  enabled: true
```

**For PostgreSQL backends**, replace the store section:

```yaml
store:
  backend: postgres
  postgres:
    dsn: postgres://grepai:grepai@localhost:5432/grepai
```

**Known issue:** PostgreSQL + pgvector has a UTF-8 encoding bug where files
containing Unicode box-drawing characters (e.g. U+2550 ═) fail to index.
GOB does not have this limitation.

**For Qdrant backends**, replace the store section:

```yaml
store:
  backend: qdrant
  qdrant:
    endpoint: http://localhost:6334
```

### Dimension Reference

| Model | Dimensions |
|-------|-----------|
| mxbai-embed-large | 1024 |
| nomic-embed-text | 768 |
| bge-m3 | 1024 |
| nomic-embed-text-v2-moe | 768 |
| text-embedding-3-small | 1536 |
| text-embedding-3-large | 3072 |

### 5. Update .gitignore

Check if `.grepai/` is in `.gitignore`. If not, append:

```text
# grepai index
.grepai/
```

### 6. Print Summary

```text
============================================================================
GrepAI Initialized
============================================================================

Config: .grepai/config.yaml

  Embedder:  {PROVIDER} / {MODEL} ({DIMS} dims)
  Storage:   {BACKEND}
  Chunking:  512 tokens, 50 overlap
  Trace:     enabled

.gitignore: ✓ .grepai/ excluded

Workspace: {NAME} (only if workspace mode, otherwise omit this line)

Next steps:
  grepai index               # Build initial index
  grepai watch --background  # Start file watcher
  /grepai:status             # Verify all components
============================================================================
```

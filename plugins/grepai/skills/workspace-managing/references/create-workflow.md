# Workspace Create Workflow

## 1. Parse Arguments

Extract workspace name from user arguments. If missing, ask. Suggest a name based on the parent directory (e.g., `~/projects/` → `projects`).

## 2. Select Backend

Ask via AskUserQuestion:

```text
Which shared backend for this workspace?

○ Qdrant — lightweight, purpose-built vector DB (Recommended)
○ PostgreSQL + pgvector — battle-tested, SQL-based
```

## 3. Select Embedding Provider

Ask via AskUserQuestion:

```text
Which embedding provider?

○ Ollama — local, private, free, works offline (Recommended)
○ OpenAI — cloud, high quality, costs per index
```

## 4. Select Embedding Model

Ask via AskUserQuestion based on provider.

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

## 5. Verify Backend Running

Check Docker for the selected backend by image or port, not container name:

**PostgreSQL:**

```bash
docker ps --filter ancestor=postgres --format "{{.Names}}\t{{.Status}}\t{{.Ports}}"
```

Or check connectivity directly:

```bash
curl -s --max-time 5 http://localhost:5432 2>&1 || echo "Port 5432 check done"
```

**Qdrant:**

Check Qdrant REST API (port 6333, not 6334 which is gRPC):

```bash
curl -s --max-time 5 http://localhost:6333/collections
```

**Ollama:**

```bash
curl -s --max-time 5 http://localhost:11434/api/tags
```

If not running, warn and suggest starting:

```text
Backend not running. Start with:
  docker compose up -d
```

## 6. Create Workspace

`grepai workspace create` is **interactive** — it prompts for backend, provider, and model sequentially. Use piped input for non-interactive creation:

**Qdrant + Ollama (most common):**

The prompt sequence is:

1. "Select storage backend:" → `2` (Qdrant)
2. "Qdrant endpoint:" → endpoint (or empty for default `http://localhost`)
3. "Qdrant port:" → port (or empty for default `6334`)
4. "Collection name:" → empty for auto
5. "Select embedding provider:" → `1` (Ollama)
6. "Ollama endpoint:" → empty for default
7. "Model:" → model name (or empty for default `nomic-embed-text`)

```bash
printf '2\n\n\n\n1\n\n{MODEL}\n' | grepai workspace create {NAME}
```

**PostgreSQL + Ollama:**

The prompt sequence is:

1. "Select storage backend:" → `1` (PostgreSQL)
2. "PostgreSQL DSN:" → DSN string
3. "Select embedding provider:" → `1` (Ollama)
4. "Ollama endpoint:" → empty for default
5. "Model:" → model name

```bash
printf '1\npostgres://grepai:grepai@localhost:5432/grepai\n1\n\n{MODEL}\n' | grepai workspace create {NAME}
```

**Qdrant + OpenAI:**

```bash
printf '2\n\n\n\n2\n{MODEL}\n' | grepai workspace create {NAME}
```

**PostgreSQL + OpenAI:**

```bash
printf '1\npostgres://grepai:grepai@localhost:5432/grepai\n2\n{MODEL}\n' | grepai workspace create {NAME}
```

If piped input fails or prompts change, fall back to reading/writing `~/.grepai/workspace.yaml` directly.

## 7. Add Projects

Ask user which directories to add as projects via AskUserQuestion. Offer contextual options:

```text
Which directories should be added to workspace {NAME}?

○ Current directory ({cwd}) (Recommended)
○ Subdirectories of {parent} — add each subfolder as a separate project
○ Custom paths — I'll specify directories
```

**If current directory:** use its absolute path:

```bash
grepai workspace add {NAME} {ABSOLUTE_CWD_PATH}
```

**If subdirectories:** list subdirectories, let user confirm which ones, then add each:

```bash
grepai workspace add {NAME} {ABSOLUTE_PATH_1}
grepai workspace add {NAME} {ABSOLUTE_PATH_2}
```

**Important:** `grepai workspace add` takes an **absolute path** and derives the project name from `filepath.Base(path)` (the directory basename).

## 8. Print Summary

```text
============================================================================
Workspace Created: {NAME}
============================================================================

Backend:   {BACKEND}
Embedder:  {PROVIDER} / {MODEL}
Projects:  {COUNT}

Add projects:   grepai workspace add {NAME} /absolute/path/to/project
List projects:  /grepai:workspace:show {NAME}
Start watcher:  grepai watch --workspace {NAME} --background
Check status:   /grepai:workspace:status {NAME}
============================================================================
```

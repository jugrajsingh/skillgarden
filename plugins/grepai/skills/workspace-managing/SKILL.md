---
name: workspace-managing
description: Manage grepai workspaces — create, add/remove projects, delete, list, show details, and check indexing status.
allowed-tools:
  - Read
  - Glob
  - Bash(grepai *)
  - Bash(docker *)
  - Bash(curl *)
  - Bash(printf *)
  - Write
  - Edit
  - AskUserQuestion
---

# GrepAI Workspace Management

Handle all workspace operations based on the `operation` parameter passed from the invoking command.

Workspaces enable cross-project semantic search with a shared vector store (PostgreSQL or Qdrant). Config lives in `~/.grepai/workspace.yaml`.

## operation=create

Create a new workspace with backend selection.

### 1. Parse Arguments

Extract workspace name from user arguments. If missing, ask:

```text
What should this workspace be called?
```

Suggest a name based on the parent directory (e.g., `~/projects/` → `projects`).

### 2. Select Backend

Workspaces require a shared vector store. Ask via AskUserQuestion:

```text
Which shared backend for this workspace?

○ Qdrant — lightweight, purpose-built vector DB (Recommended)
○ PostgreSQL + pgvector — battle-tested, SQL-based
```

### 3. Select Embedding Provider

Ask via AskUserQuestion:

```text
Which embedding provider?

○ Ollama — local, private, free, works offline (Recommended)
○ OpenAI — cloud, high quality, costs per index
```

### 4. Select Embedding Model

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

### 5. Verify Backend Running

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

### 6. Create Workspace

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

### 7. Add Projects

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

### 8. Print Summary

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

---

## operation=add

Add a project to an existing workspace.

### 1. Parse Arguments

Extract workspace name and project path. If workspace name missing, list available and ask:

```bash
grepai workspace list
```

```text
Which workspace?
```

If project path missing, default to current directory.

### 2. Add Project

Use absolute path:

```bash
grepai workspace add {WORKSPACE} {ABSOLUTE_PATH}
```

Note: grepai derives the project name from `filepath.Base(path)` (the directory basename).

### 3. Confirm

```text
Added {BASENAME} to workspace {WORKSPACE} (path: {ABSOLUTE_PATH})
```

---

## operation=remove

Remove a project from a workspace.

### 1. Parse Arguments

Extract workspace name and project name from arguments.

**Important:** `grepai workspace remove` takes the **project name** (directory basename), not the path. If the user provides a path, extract the basename.

Show current projects first so the user can identify the correct name:

```bash
grepai workspace show {WORKSPACE}
```

### 2. Remove Project

```bash
grepai workspace remove {WORKSPACE} {PROJECT_NAME}
```

### 3. Confirm

```text
Removed {PROJECT_NAME} from workspace {WORKSPACE}
```

---

## operation=delete

Delete an entire workspace.

### 1. Parse Arguments

Extract workspace name.

### 2. Confirm Deletion

Ask via AskUserQuestion:

```text
Confirm deletion of workspace {NAME}? This removes config but not indexed data.

○ Yes, delete workspace
○ No, cancel
```

If cancel, stop.

### 3. Delete Workspace

```bash
grepai workspace delete {NAME}
```

### 4. Confirm

```text
Workspace {NAME} deleted
```

---

## operation=list

List all configured workspaces.

### 1. List Workspaces

```bash
grepai workspace list
```

### 2. Format Output

Display each workspace with backend type and project count:

```text
============================================================================
GrepAI Workspaces
============================================================================

  {NAME}    backend: {TYPE}    projects: {COUNT}
  {NAME}    backend: {TYPE}    projects: {COUNT}

Manage:
  /grepai:workspace:show {NAME}     View details
  /grepai:workspace:create {NAME}   Create new
============================================================================
```

---

## operation=show

Show workspace details and projects.

### 1. Parse Arguments

Extract workspace name.

### 2. Show Details

```bash
grepai workspace show {NAME}
```

Optionally also read `~/.grepai/workspace.yaml` for additional detail if CLI output is sparse.

### 3. Format Output

```text
============================================================================
Workspace: {NAME}
============================================================================

Backend:   {TYPE}
Embedder:  {PROVIDER} / {MODEL}

Projects:
  {PROJECT_1}    {PATH_1}
  {PROJECT_2}    {PATH_2}

Commands:
  /grepai:workspace:add {NAME} /path     Add project
  /grepai:workspace:remove {NAME} proj   Remove project
  /grepai:workspace:status {NAME}        Check index health
============================================================================
```

---

## operation=status

Show workspace indexing status.

### 1. Parse Arguments

Extract optional workspace name. If omitted, check all workspaces.

### 2. Check Status

```bash
grepai workspace status {NAME}
```

Or for all:

```bash
grepai workspace status
```

### 3. Check Watcher

```bash
grepai watch --workspace {NAME} --status
```

### 4. Format Output

```text
============================================================================
Workspace Status: {NAME}
============================================================================

Backend:  {TYPE} — {STATUS}

Projects:
  {S} {PROJECT_1}    {FILES} files, {CHUNKS} chunks    last: {TIMESTAMP}
  {S} {PROJECT_2}    {FILES} files, {CHUNKS} chunks    last: {TIMESTAMP}

Watcher:  {RUNNING|STOPPED}

============================================================================
```

Where {S} is one of: OK for indexed, FAIL for failed, STALE for stale/partial.

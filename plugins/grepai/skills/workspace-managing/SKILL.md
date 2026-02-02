---
name: workspace-managing
description: Manage grepai workspaces — create, add/remove projects, delete, list, show details, and check indexing status.
allowed-tools:
  - Read
  - Glob
  - Bash(grepai *)
  - Bash(docker *)
  - Bash(curl *)
  - Write
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

○ PostgreSQL + pgvector — battle-tested, SQL-based (Recommended)
○ Qdrant — lightweight, purpose-built vector DB
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

Check Docker for the selected backend container:

**PostgreSQL:**

```bash
docker ps --filter name=grepai-postgres --format "{{.Status}}"
```

**Qdrant:**

```bash
docker ps --filter name=grepai-qdrant --format "{{.Status}}"
```

If not running, warn and suggest starting with the appropriate template:

```text
Backend not running. Start with:
  docker compose -f docker-compose-{postgres|qdrant}.yml up -d
```

### 6. Create Workspace

```bash
grepai workspace create {NAME} --backend {postgres|qdrant} --provider {ollama|openai} --model {MODEL}
```

If the CLI requires interactive input, construct config directly by reading/writing `~/.grepai/workspace.yaml`.

### 7. Add Current Project

Ask via AskUserQuestion:

```text
Add current project to workspace {NAME}?

○ Yes, add this project (Recommended)
○ No, I'll add projects later
```

If yes:

```bash
grepai workspace add {NAME} .
```

### 8. Print Summary

```text
============================================================================
Workspace Created: {NAME}
============================================================================

Backend:   {postgres|qdrant}
Embedder:  {PROVIDER} / {MODEL}
Projects:  {COUNT}

Add projects:   grepai workspace add {NAME} /path/to/project
List projects:  /grepai:workspace:show {NAME}
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

```bash
grepai workspace add {WORKSPACE} {PATH}
```

### 3. Confirm

```text
✓ Added {PATH} to workspace {WORKSPACE}
```

---

## operation=remove

Remove a project from a workspace.

### 1. Parse Arguments

Extract workspace name and project name from arguments.

### 2. Remove Project

```bash
grepai workspace remove {WORKSPACE} {PROJECT}
```

### 3. Confirm

```text
✓ Removed {PROJECT} from workspace {WORKSPACE}
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
✓ Workspace {NAME} deleted
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

### 3. Format Output

```text
============================================================================
Workspace: {NAME}
============================================================================

Backend:   {TYPE}
Embedder:  {PROVIDER} / {MODEL}

Projects:
  ✓ {PROJECT_1}    {PATH_1}
  ✓ {PROJECT_2}    {PATH_2}

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

Where {S} is ✓ for indexed, ✗ for failed, △ for stale/partial.

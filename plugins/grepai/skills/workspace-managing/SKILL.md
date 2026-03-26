---
name: workspace-managing
description: Use when you need to create, modify, or inspect GrepAI workspaces and their project associations
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

Create a new workspace with backend and embedding selection. Parse workspace name from args (suggest parent directory name if missing). Ask for backend (Qdrant recommended, PostgreSQL), embedding provider (Ollama recommended, OpenAI), and model. Verify backend running via Docker/curl. Create workspace using piped `printf` input to `grepai workspace create` (interactive CLI). Add projects by absolute path. Print summary with commands.

See references/create-workflow.md for backend selection prompts, printf sequences for all 4 backend+provider combinations, project addition flow, and summary template.

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

Run `grepai workspace list`. Display each workspace with backend type and project count. See references/output-templates.md for list format.

---

## operation=show

Extract workspace name. Run `grepai workspace show {NAME}` (optionally read `~/.grepai/workspace.yaml` for detail). Display backend, embedder, projects, and management commands. See references/output-templates.md for show format.

---

## operation=status

Extract optional workspace name (`grepai workspace status {NAME}` or all). Check watcher (`grepai watch --workspace {NAME} --status`). Display backend status, per-project index health (OK/FAIL/STALE), and watcher state. See references/output-templates.md for status format.

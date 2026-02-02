---
name: initializing
description: Initialize grepai in a project — run grepai init, configure provider/model/storage in .grepai/config.yaml, and update .gitignore.
allowed-tools:
  - Read
  - Glob
  - Bash(grepai *)
  - Edit
  - Write
  - AskUserQuestion
  - Skill
---

# GrepAI Project Initialization

Initialize grepai config for the current project with the chosen embedding provider, model, and storage backend.

## Context

This skill expects context from the `grepai:setting-up` skill:

- **provider**: ollama or openai
- **model**: embedding model name
- **backend**: postgres, qdrant, or gob
- **workspace_name**: workspace name (if workspace mode)

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

1. Determine which directory to add as the project. Ask via AskUserQuestion:

   ```text
   Which directory should be added to the workspace?

   ○ Current directory ({cwd}) (Recommended)
   ○ Parent directory ({parent}) — if it contains multiple project subdirectories
   ○ Custom path
   ```

2. Ask for workspace name (suggest based on parent directory name)
3. Check if workspace exists:

   ```bash
   grepai workspace list
   ```

4. If new workspace: invoke the `grepai:workspace-managing` skill with operation=create, then return here
5. If existing workspace: add the chosen directory:

   ```bash
   grepai workspace add {NAME} {ABSOLUTE_PATH}
   ```

   Note: grepai derives the project name from `filepath.Base(path)`.

6. Still run steps 1-5 below for per-project config (chunking, ignore patterns, MCP anchor)
7. In the summary (step 6), note workspace membership and add CLAUDE.md guidance

**If single project:** continue with step 1.

### 1. Check Existing Config

```text
Glob: .grepai/config.yaml
```

If `.grepai/` exists, warn:

```text
Existing .grepai/config.yaml found. Reinitializing will overwrite it.
```

Ask via AskUserQuestion:

```text
Existing grepai config found. What to do?

○ Overwrite — reinitialize with new settings (Recommended)
○ Cancel — keep existing config
```

If cancel, stop.

### 2. Run grepai init (non-interactive)

Use `--yes` flag with provider and backend flags to avoid interactive prompts:

```bash
grepai init --yes -p {PROVIDER} -b {BACKEND}
```

Where:

- `{PROVIDER}` is `ollama` or `openai`
- `{BACKEND}` is `gob`, `postgres`, or `qdrant`

This creates `.grepai/config.yaml` with defaults and auto-adds `.grepai/` to `.gitignore`.

**For workspace mode:** always use GOB for the local config since the workspace handles the shared store separately:

```bash
grepai init --yes -p ollama -b gob
```

### 3. Adjust Model if Needed

Read the generated config:

```text
Read: .grepai/config.yaml
```

If the chosen model differs from the default (`nomic-embed-text` for Ollama), edit the config to set the correct model and dimensions:

```text
Edit: .grepai/config.yaml
  embedder.model: {MODEL}
  embedder.dimensions: {DIMS}
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

### 4. Verify .gitignore

`grepai init` auto-adds `.grepai/` to `.gitignore`. Verify it was added:

```text
Read: .gitignore
```

If `.gitignore` does not exist or `.grepai/` is missing from it, append:

```text
# grepai index
.grepai/
```

### 5. CLAUDE.md Workspace Guidance (workspace mode only)

When workspace mode is active, append workspace usage instructions to the project's CLAUDE.md (or AGENTS.md) so agents know to use workspace search parameters with the MCP tool:

```markdown
## grepai Workspace

This project is part of the `{WORKSPACE}` grepai workspace.
When using the `grepai_search` MCP tool, pass `workspace="{WORKSPACE}"` to search across all workspace projects.
Use `projects="{PROJECT_NAME}"` to narrow results to a specific project.
```

If CLAUDE.md does not exist, create it with just this section. If it exists, append the section (checking it doesn't already have a grepai workspace section).

### 6. Print Summary

```text
============================================================================
GrepAI Initialized
============================================================================

Config: .grepai/config.yaml

  Embedder:  {PROVIDER} / {MODEL} ({DIMS} dims)
  Storage:   {BACKEND}
  Chunking:  512 tokens, 50 overlap

.gitignore: .grepai/ excluded

Workspace: {NAME} (only if workspace mode, otherwise omit this line)
CLAUDE.md:  workspace guidance added (only if workspace mode)

Next steps:
  grepai index               # Build initial index
  grepai watch --background  # Start file watcher (single project)
  grepai watch --workspace {NAME} --background  # Start workspace watcher
  /grepai:status             # Verify all components
============================================================================
```

---
name: initializing
description: Use when a project needs GrepAI initialized with config file and gitignore setup
allowed-tools:
  - Read
  - Glob
  - Bash(grepai *)
  - Edit
  - Write
  - Skill
  - AskUserQuestion
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

When invoked standalone (not from setting-up skill), ask scope: single project (recommended) or workspace (requires PostgreSQL/Qdrant). If workspace: ask directory, workspace name, create or add to workspace via `grepai:workspace-managing` skill, then continue with steps 1-5 for per-project config.

See references/workspace-setup.md for scope prompts, workspace creation flow, and CLAUDE.md guidance.

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

Append workspace usage instructions to CLAUDE.md so agents use workspace search parameters with MCP tool. See references/workspace-setup.md for the CLAUDE.md template.

### 6. Print Summary

Print config summary with embedder, storage, gitignore status, workspace membership, and next steps. See references/workspace-setup.md for the summary template.

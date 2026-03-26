# Workspace Setup During Initialization

## Project Scope Selection

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

## CLAUDE.md Workspace Guidance (workspace mode only)

When workspace mode is active, append workspace usage instructions to the project's CLAUDE.md (or AGENTS.md) so agents know to use workspace search parameters with the MCP tool:

```markdown
## grepai Workspace

This project is part of the `{WORKSPACE}` grepai workspace.
When using the `grepai_search` MCP tool, pass `workspace="{WORKSPACE}"` to search across all workspace projects.
Use `projects="{PROJECT_NAME}"` to narrow results to a specific project.
```

If CLAUDE.md does not exist, create it with just this section. If it exists, append the section (checking it doesn't already have a grepai workspace section).

## Summary Template

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

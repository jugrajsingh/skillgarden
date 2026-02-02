---
name: mcp-setup
description: Configure grepai MCP server for Claude Code, Cursor, or Windsurf with scope and workspace options.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash(claude *)
  - Bash(which *)
  - Bash(cat *)
  - Write
  - Edit
  - AskUserQuestion
---

# GrepAI MCP Server Configuration

Configure grepai as an MCP server for AI coding assistants. Supports multiple IDEs, scopes, and workspace modes.

## Workflow

### 1. Detect Current State

Check all possible MCP registration locations and grepai config:

```bash
# Check existing MCP registrations
claude mcp list 2>/dev/null
```

```text
Glob: .mcp.json
Glob: .claude/mcp.json
Read: ~/.claude.json  (look for mcpServers section)
```

Check for workspaces:

```bash
grepai workspace list 2>/dev/null
```

Check for local project config:

```text
Glob: .grepai/config.yaml
```

Summarize findings before proceeding:

- Existing MCP registrations (if any)
- Available workspaces (if any)
- Local project config (if any)
- grepai binary location: `which grepai`

### 2. Ask: IDE Target

Ask via AskUserQuestion:

```text
Which IDE to configure?

○ Claude Code (Recommended)
○ Cursor
○ Windsurf
○ Generic .mcp.json
```

### 3. Ask: Registration Scope

**For Claude Code**, ask via AskUserQuestion:

```text
Where should the MCP server be registered?

○ Project .mcp.json (Recommended for teams — shareable via git)
○ User global (~/.claude.json — available in all sessions)
○ Project .claude/mcp.json (this project only, not shared)
```

**For Cursor:** config goes to `.cursor/mcp.json` (project-level).

**For Windsurf:** config goes to `.windsurf/mcp.json` (project-level).

**For Generic:** config goes to `.mcp.json` at project root.

### 4. Ask: Workspace Mode

Only ask this if workspaces were detected in step 1.

Ask via AskUserQuestion:

```text
Workspace mode?

○ With --workspace {NAME} (Recommended — auto-searches all projects without extra params)
○ Without workspace (agent must pass workspace parameter manually)
○ No workspace (single project mode)
```

If workspace selected, show the available workspaces and let user pick:

```text
Which workspace?

○ {ws1} ({N} projects)
○ {ws2} ({N} projects)
```

### 5. Generate Configuration

Determine the grepai binary path:

```bash
which grepai
```

#### For Claude Code — `claude mcp add`

**User scope:**

```bash
claude mcp add grepai -s user -- grepai mcp-serve {ARGS}
```

**Project scope:**

```bash
claude mcp add grepai -s project -- grepai mcp-serve {ARGS}
```

**Where `{ARGS}` is:**

- No workspace: empty (auto-detects from cwd)
- With workspace: `--workspace {NAME}`
- With explicit path: `{PROJECT_PATH}`

#### For `.mcp.json` (project root, Cursor, Windsurf, Generic)

Determine the target file:

- Cursor: `.cursor/mcp.json`
- Windsurf: `.windsurf/mcp.json`
- Generic / Project .mcp.json: `.mcp.json`

Write the JSON config:

```json
{
  "mcpServers": {
    "grepai": {
      "command": "grepai",
      "args": ["mcp-serve"]
    }
  }
}
```

**With workspace:**

```json
{
  "mcpServers": {
    "grepai": {
      "command": "grepai",
      "args": ["mcp-serve", "--workspace", "{NAME}"]
    }
  }
}
```

**With explicit project path:**

```json
{
  "mcpServers": {
    "grepai": {
      "command": "grepai",
      "args": ["mcp-serve", "{PROJECT_PATH}"]
    }
  }
}
```

If the target JSON file already exists, read it first and merge the `grepai` key into the existing `mcpServers` object. Do not overwrite other MCP servers.

#### Create parent directories if needed

```bash
mkdir -p .cursor   # for Cursor
mkdir -p .windsurf # for Windsurf
```

### 6. Add to .gitignore (if applicable)

For project-level `.mcp.json` files that teams share, do NOT gitignore them.

For `.claude/mcp.json` (project-specific, not shared), check if `.claude/` is in `.gitignore`. If not, suggest adding it.

### 7. Verify

**For Claude Code:**

```bash
claude mcp list
```

Confirm `grepai` appears in the list.

**For file-based configs:**

Read the written file to confirm it's valid JSON.

Note: The MCP server connects on next IDE session start, not immediately.

### 8. Print Summary

```text
============================================================================
GrepAI MCP Server Configured
============================================================================

IDE:        {IDE}
Scope:      {SCOPE}
Config:     {FILE_PATH}
Command:    grepai mcp-serve {ARGS}
Workspace:  {NAME or "none"}

The MCP server will be available in your next {IDE} session.
It exposes these tools:

  grepai_search         — Semantic code search
  grepai_trace_callers  — Find all callers of a function
  grepai_trace_callees  — Find all callees of a function
  grepai_trace_graph    — Build call graph around a symbol
  grepai_index_status   — Check index health

{IF WORKSPACE}
Workspace mode is enabled. The agent will automatically search
across all {N} projects in the "{NAME}" workspace without needing
to specify the workspace parameter.
{END IF}

To verify after restart:
  claude mcp list       # Claude Code
============================================================================
```

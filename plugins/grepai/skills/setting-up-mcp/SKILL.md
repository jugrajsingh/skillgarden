---
name: setting-up-mcp
description: Use when you need to register or update the GrepAI MCP server in Claude Code, Cursor, or Windsurf
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

Determine grepai binary path (`which grepai`). For Claude Code: use `claude mcp add` with scope (user/project) and optional `--workspace {NAME}`. For Cursor/Windsurf/Generic: write JSON to IDE-specific `.mcp.json` file, merging into existing config if present.

See references/mcp-configs.md for `claude mcp add` commands, JSON templates (basic, workspace, explicit path), and IDE target file paths.

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

Print IDE, scope, config path, command, workspace status, exposed MCP tools, and verification command. See references/mcp-configs.md for the summary template.

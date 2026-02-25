# MCP Configuration Templates

## For Claude Code — `claude mcp add`

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

## For .mcp.json (Cursor, Windsurf, Generic)

Target files:

- Cursor: `.cursor/mcp.json`
- Windsurf: `.windsurf/mcp.json`
- Generic / Project .mcp.json: `.mcp.json`

**Basic config:**

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

Create parent directories if needed:

```bash
mkdir -p .cursor   # for Cursor
mkdir -p .windsurf # for Windsurf
```

## Summary Template

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

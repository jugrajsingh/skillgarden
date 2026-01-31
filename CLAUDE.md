# Claude Code Project Guide

## Purpose

SkillGarden is a Claude Code plugin marketplace for skills and tools used in day-to-day development. This repository follows git-flow workflow with branch protection enforced via pre-commit hooks.

## Development Setup

**Before developing, read [CONTRIBUTING.md](CONTRIBUTING.md)** for git-flow workflow and pre-commit setup.

## Structure

```text
skillgarden/
├── .claude-plugin/
│   └── marketplace.json          # Central plugin registry
├── plugins/
│   └── <plugin-name>/
│       ├── .claude-plugin/
│       │   └── plugin.json       # Plugin manifest (required)
│       ├── commands/             # Thin wrappers → skills
│       ├── skills/               # Actual logic (SKILL.md)
│       ├── agents/               # Specialized agents
│       └── hooks/                # Event handlers (hooks.json)
├── .pre-commit-config.yaml       # Branch protection + linting
└── CLAUDE.md                     # This file
```

## Plugin Development Best Practices

### Supported Plugin Directories

| Directory | Purpose |
|-----------|---------|
| `.claude-plugin/` | Only `plugin.json` manifest (required) |
| `commands/` | Skills as Markdown files |
| `skills/` | Agent Skills with `SKILL.md` files |
| `agents/` | Custom agent definitions |
| `hooks/` | Event handlers in `hooks.json` |
| `.mcp.json` | MCP server configurations |
| `.lsp.json` | LSP server configurations |

Note: `rules/` is NOT supported in plugins. Rules go in `.claude/rules/` at project/user level.

### Command vs Skill Pattern

Commands are thin wrappers that delegate to skills. Skills contain actual logic.

**Command** (`commands/my-command.md`):

```yaml
---
name: plugin:my-command
description: Short description
argument-hint: "<arg>"
---

# This command MUST invoke the `plugin-my-skill` skill.
Pass the user request to the skill.
```

**Skill** (`skills/my-skill/SKILL.md`):

```yaml
---
name: plugin-my-skill
description: Detailed description of what this skill does
---

# Skill Title
[Workflow logic - keep under 500 lines, use references/ for overflow]
```

### Environment Variables

| Variable | Available In | Purpose |
|----------|-------------|---------|
| `${CLAUDE_PLUGIN_ROOT}` | plugin.json | Plugin installation directory |
| `$CLAUDE_PROJECT_DIR` | Hook scripts | User's project root |
| `$file` | PostToolUse hooks | Affected file path |

Syntax:

- Config files (plugin.json): `${VARIABLE}` with braces
- Shell scripts: `$VARIABLE` (standard shell)

### Hook Patterns

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/scripts/my-guard.sh",
        "timeout": 5
      }]
    }]
  }
}
```

## Formatting Conventions

### Concision

Sacrifice grammar for concision. Goal is density, not minimalism.

Good: "Ask one question, wait for response"
Bad: "Ask question wait response"

### Variables

- `{VARIABLE}` — concrete placeholder (all caps)
- `{ description }` — instructional prose (lowercase, spaces)

### Indicators

Prefer ASCII/Unicode over emoji for terminal output:

| Use | Symbol | Purpose |
|-----|--------|---------|
| Progress | `▓▓▓░░` | 3/5 completion |
| Severity | `◇ ◆ ◆◆` | Minor → Severe |
| Caveat | `△` | Incomplete/uncertain |
| Done | `✓` | Completed item |
| Recommend | `★` | Preferred option |

### Skill References

- Standard: "Load the `plugin:skill-name` skill"
- Delegated: "Delegate by loading the `plugin:skill-name` skill"
- Never link to SKILL.md files directly

## Versioning

Use semver. Bump version when skill/agent/command files change:

- `plugins/<plugin>/skills/**/*.md`
- `plugins/<plugin>/agents/**/*.md`
- `plugins/<plugin>/commands/**/*.md`

Don't bump for pure README/doc changes.

When bumping, update:

- `.claude-plugin/marketplace.json` → plugin version
- `plugins/<plugin>/.claude-plugin/plugin.json` → version

## Editing Rules

- Keep prompts concise and direct
- Avoid feature flags or backwards-compatibility scaffolding
- Do not add extra commands/agents/skills unless explicitly requested
- SKILL.md files should be < 500 lines; use `references/` for overflow

## Testing

```bash
# Validate JSON manifests
jq . .claude-plugin/marketplace.json
jq . plugins/<plugin>/.claude-plugin/plugin.json

# Test plugin locally
claude --plugin-dir ./plugins/<plugin>
```

## Repo Metadata

- Author: Jugraj Singh (<jugrajskhalsa@gmail.com>)

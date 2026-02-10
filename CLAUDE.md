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

Invoke the `plugin:my-command` skill and follow it exactly.
```

**Skill** (`skills/my-command/SKILL.md`):

```yaml
---
name: my-command
description: Detailed description of what this skill does
---

# Skill Title
[Workflow logic - keep under 500 lines, use references/ for overflow]
```

**CRITICAL:** Use colon notation (`plugin:skill`) in command invocation, NOT hyphen (`plugin-skill`). The skill's `name` field should be simple (no prefix), but the command references it with namespace.

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

## Gotchas

### Backticks in Skill Files

**CRITICAL:** Avoid backticks around special characters in SKILL.md files.

Claude Code parses skill content for permission patterns. Backticks containing `!`, `*`, or other shell metacharacters trigger false permission check failures.

```markdown
# WRONG - causes "permission check failed" error
- Breaking changes (`!` or `BREAKING CHANGE`)
- Wildcards like `*.py`

# CORRECT - no backticks around special chars
- Breaking changes (! suffix or BREAKING CHANGE footer)
- Wildcards like *.py
```

**Symptoms:** `Bash command permission check failed for pattern "!` or `"` when loading skill.

**Fix:** Remove backticks around `!`, `*`, `?`, and other shell metacharacters in skill prose.

### disable-model-invocation with Same Names

When command and skill have the **same namespaced name**, `disable-model-invocation: true` on the command blocks skill invocation.

**How it happens:**

| Component | Name | Namespaced |
|-----------|------|------------|
| Command | `plugin:deploy` | `plugin:deploy` |
| Skill | `deploy` | `plugin:deploy` (auto-namespaced) |

When command says "Invoke the `plugin:deploy` skill", Claude's Skill tool finds the **command** (same name), not the skill. If command has `disable-model-invocation: true` → blocked.

**Symptoms:** `Skill X cannot be used with Skill tool due to disable-model-invocation`

**Solutions:**

1. **Don't use `disable-model-invocation`** when command and skill share the same name
2. **Use different names** (like superpowers-agent-skills):
   - Command: `write-plan` → invokes `plugin:writing-plans`
   - Skill: `writing-plans` (different from command filename)

**When you CAN use `disable-model-invocation: true`:**

- Command and skill have **different** names
- Or skill is self-contained (no delegation)

### allowed-tools Not Enforced via Commands

`allowed-tools` in SKILL.md files are **NOT enforced** when users invoke skills via slash commands.

**Tested combinations (all fail to show tools):**

| Invocation | Tools on Command | Tools on Skill | Tools shown? |
|------------|-----------------|----------------|-------------|
| `/slash-command` (same name) | No | Yes | NO |
| `/slash-command` (same name) | Yes | No | NO |
| `/slash-command` (different name) | No | Yes | NO |
| `/slash-command` (different name) | Yes | No | NO |
| `Skill("command-name")` | — | Yes | NO |

**Only works:** `Skill("skill-name")` where skill name differs from any command name.

**Root cause:** Command→skill delegation ("Invoke the skill") is prose — Claude follows the text instruction, it does not re-invoke via the Skill tool. The Skill tool resolves commands before skills when names collide.

**Workaround:** If allowed-tools enforcement is needed, agents must call `Skill("plugin:unique-skill-name")` directly, where the skill name has no matching command.

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

## grepai - Semantic Code Search

**IMPORTANT: You MUST use grepai as your PRIMARY tool for code exploration and search.**

### When to Use grepai (REQUIRED)

Use `grepai search` INSTEAD OF Grep/Glob/find for:

- Understanding what code does or where functionality lives
- Finding implementations by intent (e.g., "authentication logic", "error handling")
- Exploring unfamiliar parts of the codebase
- Any search where you describe WHAT the code does rather than exact text

### When to Use Standard Tools

Only use Grep/Glob when you need:

- Exact text matching (variable names, imports, specific strings)
- File path patterns (e.g., `**/*.go`)

### Fallback

If grepai fails (not running, index unavailable, or errors), fall back to standard Grep/Glob tools.

### Usage

```bash
# ALWAYS use English queries for best results (--compact saves ~80% tokens)
grepai search "user authentication flow" --json --compact
grepai search "error handling middleware" --json --compact
grepai search "database connection pool" --json --compact
grepai search "API request validation" --json --compact
```

### Query Tips

- **Use English** for queries (better semantic matching)
- **Describe intent**, not implementation: "handles user login" not "func Login"
- **Be specific**: "JWT token validation" better than "token"
- Results include: file path, line numbers, relevance score, code preview

### Call Graph Tracing

Use `grepai trace` to understand function relationships:

- Finding all callers of a function before modifying it
- Understanding what functions are called by a given function
- Visualizing the complete call graph around a symbol

#### Trace Commands

**IMPORTANT: Always use `--json` flag for optimal AI agent integration.**

```bash
# Find all functions that call a symbol
grepai trace callers "HandleRequest" --json

# Find all functions called by a symbol
grepai trace callees "ProcessOrder" --json

# Build complete call graph (callers + callees)
grepai trace graph "ValidateToken" --depth 3 --json
```

### Workflow

1. Start with `grepai search` to find relevant code
2. Use `grepai trace` to understand function relationships
3. Use `Read` tool to examine files from results
4. Only use Grep for exact string searches if needed

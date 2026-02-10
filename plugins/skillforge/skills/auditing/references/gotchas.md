# Skill Authoring Gotchas

Known pitfalls discovered through real-world skill development. Check every skill against these.

## How Claude Code Resolves Skills

**This is foundational — misunderstanding this causes multiple downstream errors.**

### Folder Name vs Frontmatter Name

| Property | Purpose | Affects Resolution? |
|----------|---------|-------------------|
| Folder name (`skills/commit/`) | File discovery — Claude scans for `skills/*/SKILL.md` | No |
| Frontmatter `name` field | Identifies the skill for invocation | **Yes** |

Claude auto-discovers skills by scanning `skills/` subdirectories for SKILL.md files. The `name` in frontmatter is what identifies the skill. The folder name is purely organizational.

- Renaming folder from `commit/` to `committing/` → no effect on resolution
- Changing frontmatter `name: commit` to `name: committing` → changes the skill identity

**Best practice:** Use meaningful folder names that match the skill's purpose (e.g., `auditing/`, `generating-deploy/`). This is for human readability, not for Claude.

### allowed-tools Lives on Skills (Not Commands)

`allowed-tools` works on both skills and commands. The canonical placement is on the **skill** where the logic lives.

| Component | Frontmatter Fields |
|-----------|-------------------|
| Skill (`skills/*/SKILL.md`) | name, description, allowed-tools, disable-model-invocation |
| Command (`commands/*.md`) | name, description, argument-hint, allowed-tools, disable-model-invocation, model |

Both skills and commands appear in the `/` autocomplete:

- Skill `/auditing (plugin)` — from `skills/auditing/SKILL.md`
- Command `/plugin:audit` — from `commands/audit.md`

**Canonical pattern — allowed-tools on the skill:**

```yaml
# skills/commit/SKILL.md
---
name: commit
description: Create atomic commits
allowed-tools:
  - Bash(git *)
  - AskUserQuestion
---
```

```yaml
# commands/commit.md (thin wrapper, no allowed-tools needed)
---
name: plugin:commit
description: Create atomic commits
argument-hint: "[files...]"
---

Invoke the `plugin:commit` skill and follow it exactly.
```

**Why on the skill:** Tools are granted when Claude auto-invokes OR when user types the command. On commands, tools are only granted via explicit `/command` invocation.

Commands are optional thin wrappers for: `argument-hint`, `disable-model-invocation`, or `model` override.

## Backticks Around Shell Metacharacters

**Severity:** Critical — breaks skill loading entirely

Claude Code parses skill content for permission patterns. Backticks containing `!`, `*`, `?`, or other shell metacharacters trigger false permission check failures.

**Symptoms:**

- `Bash command permission check failed for pattern "!` when loading skill
- Skill refuses to load or throws permission errors

**Wrong:**

```markdown
- Breaking changes (`!` or `BREAKING CHANGE`)
- Wildcards like `*.py`
- Optional flags (`?=`)
```

**Correct:**

```markdown
- Breaking changes (! suffix or BREAKING CHANGE footer)
- Wildcards like *.py
- Optional flags (?=)
```

**Rule:** Never wrap shell metacharacters in backticks within SKILL.md prose. Code blocks (triple backtick fences) are fine — the issue is inline backticks only.

**Safe in reference files:** Reference files loaded via Read tool at runtime bypass the skill parser entirely. You can safely document backticked metacharacters in reference files.

## Command-Skill Name Collision with disable-model-invocation

**Severity:** Critical — but ONLY when disable-model-invocation is used

When command and skill share the same namespaced name AND the command has `disable-model-invocation: true`, the Skill tool finds the command instead of the skill and blocks it.

**How names resolve:**

| Component | Frontmatter Name | Resolved Name |
|-----------|-----------------|---------------|
| Command `commands/deploy.md` | `plugin:deploy` | `plugin:deploy` |
| Skill `skills/deploy/SKILL.md` | `deploy` | `plugin:deploy` (auto-namespaced) |

**Note:** The folder name (`skills/deploy/`) does NOT affect resolution. Only the frontmatter `name: deploy` matters.

**When this is a problem:**

- Command has `disable-model-invocation: true` AND same resolved name as skill → blocked

**When this is NOT a problem:**

- Same names but no `disable-model-invocation` → works fine (most common case)

**Solutions if you need disable-model-invocation:**

1. Use different frontmatter names: command `deploy` → skill `generating-deploy`
2. Or just don't use `disable-model-invocation`

## Variable Placeholder Syntax

**Severity:** Medium — causes confusion

Two syntaxes exist and must not be mixed:

| Syntax | Meaning | Where |
|--------|---------|-------|
| `{VARIABLE}` (all caps) | Concrete placeholder to be replaced | Templates, generated files |
| `{ description }` (lowercase, spaces) | Instructional prose | Workflow descriptions |
| `${VARIABLE}` (with dollar) | Environment variable | plugin.json, shell scripts |

## Formatting

### ASCII Over Emoji

Skills should use ASCII/Unicode indicators for terminal compatibility:

| Use | Symbol | Not |
|-----|--------|-----|
| Done | `✓` | :white_check_mark: |
| Failed | `✗` | :x: |
| Progress | `▓▓▓░░` | progress bar emoji |
| Severity | `◇ ◆ ◆◆` | colored circles |
| Caveat | `△` | warning emoji |
| Recommend | `★` | star emoji |

### Concision

Sacrifice grammar for density. Not minimalism — concision.

**Good:** "Ask one question, wait for response"
**Bad:** "Ask question wait response"
**Also bad:** "You should then ask the user a single question and wait for their response before proceeding"

## allowed-tools Scope Creep

**Severity:** Low — wastes permissions

Skills should request minimal tools. Common over-requests:

| Over-requested | When actually needed |
|---------------|---------------------|
| `Bash` (unrestricted) | Only if running arbitrary commands |
| `Bash(command *)` | Only if that specific command is used |
| `Write` | Only if the skill creates/modifies files |
| `Grep` | Only if the skill searches file contents (not just file names) |
| `Skill` | Only for orchestrator skills that delegate |

## Skill Reference Syntax

When one skill invokes another:

**Wrong:**

```markdown
Read the skill at `skills/generating-dockerfile/SKILL.md`
Load `../generating-dockerfile/SKILL.md`
```

**Correct:**

```markdown
Invoke the `dockercraft:generating-dockerfile` skill and follow it exactly.
```

Always use colon notation (`plugin:skill`), never file paths.

## One-to-Many Deployments vs Pipelines

**Severity:** Low — terminology confusion

When the same codebase deploys as multiple releases (same image, different configs), call these "deployments" not "pipelines":

- **Deployments:** Same code, multiple Helm releases (service-type1, service-type2)
- **Pipelines:** Different processing stages (ingest → transform → load)

Use "one-to-many deployments" to describe the pattern where one build produces multiple deployment targets.

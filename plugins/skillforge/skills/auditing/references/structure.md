# Skill Structure Checklist

## Frontmatter

### SKILL.md Frontmatter

Skills support `name`, `description`, `allowed-tools`, and `disable-model-invocation`:

```yaml
---
name: skill-name          # Simple name, no plugin prefix
description: What it does  # One line, used in skill listing
allowed-tools:
  - Read
  - Glob
  - AskUserQuestion
---
```

`allowed-tools` on a skill grants Claude access to those tools without per-use approval when the skill is active. This is the canonical location for tool permissions.

### Command Frontmatter (thin wrapper)

Commands provide `argument-hint` and user-facing `/` entry point. Tool permissions belong on the skill, not here:

```yaml
---
name: plugin:command-name
description: Short description
argument-hint: "[args]"
---

Invoke the `plugin:skill-name` skill and follow it exactly.
```

### allowed-tools Rules

- Only list tools the skill actually needs
- Bash requires pattern: `Bash(command-prefix *)` not bare `Bash`
- `Skill` tool only for orchestrator skills that delegate to other skills
- Common sets:
  - Generator: Read, Write, Glob, AskUserQuestion
  - Auditor: Read, Glob, Grep, AskUserQuestion
  - Orchestrator: Read, Glob, AskUserQuestion, Skill

## Workflow Pattern

Skills follow a detect-confirm-generate-report pattern:

### 1. Detection Phase

Discover project context before acting. Never assume — detect:

```text
Glob: pyproject.toml, package.json, go.mod, Cargo.toml
```

Map detection results to decisions (language, services, deployment method).

### 2. Confirmation Phase

Present detected choices to user via AskUserQuestion before generating anything.

Multi-select for additive choices (services):

```text
☑ postgres (asyncpg found)
☑ redis (redis found)
☐ elasticsearch
```

Single-select for exclusive choices (deployment method):

```text
○ Helm (Kubernetes via Helm charts)
○ kubectl (direct Kubernetes manifests)
```

### 3. Generation Phase

Generate files using confirmed choices. Load reference files only for confirmed selections.

### 4. Report Phase

Every skill ends with a summary report:

```text
Created {file}:

Configuration:
  - {key}: {value}

Commands:
  {command}  # {description}
```

## Naming Conventions

### Skill Names

| Pattern | When | Example |
|---------|------|---------|
| `generating-{thing}` | Creates a file | `generating-dockerfile` |
| `auditing` | Evaluates against checklist | `auditing` |
| `optimizing` | Improves existing | `optimizing` |
| `setting-up` | Orchestrates multiple generators | `setting-up` |

### Command Names

Commands are thin wrappers. Use short verb forms:

| Skill Name | Command Name |
|------------|-------------|
| `generating-dockerfile` | `dockerfile` |
| `generating-compose` | `compose` |
| `auditing` | `audit` |
| `setting-up` | `setup` |

### Command-Skill Name Collision

If command filename matches skill name after namespacing, `disable-model-invocation: true` on the command will block the skill. Use different names:

| Command | Skill | Collision? |
|---------|-------|-----------|
| `deploy.md` | `deploy` | Yes — both resolve to `plugin:deploy` |
| `deploy.md` | `generating-deploy` | No — different names |

## Orchestrator Skills

Skills that delegate to other skills (like `setting-up`):

- Include `Skill` in allowed-tools
- Reference other skills by namespaced name: "Invoke the `plugin:skill-name` skill"
- Never link to SKILL.md files directly
- Check for existing files before delegating (avoid overwriting)

## Philosophy Section

Optional but recommended. 3-6 bullet points establishing design principles:

```markdown
## Philosophy

- **Principle name** - Brief explanation
- **Another principle** - Brief explanation
```

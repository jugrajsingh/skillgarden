# Orchestrator Skill Template

Orchestrator skills coordinate multiple generator skills in sequence, checking for existing files and delegating.

## SKILL.md Template

```yaml
---
name: setting-up
description: Set up complete {thing} environment by orchestrating {sub-skills}.
allowed-tools:
  - Read
  - Glob
  - Bash({relevant_commands} *)
  - AskUserQuestion
  - Skill
---
```

```markdown
# {Thing} Setup (Orchestrator)

Orchestrates {thing} setup by invoking specialized skills.

## What Gets Set Up

1. **{Component 1}** - {description}
2. **{Component 2}** - {description}
3. **{Component 3}** - {description}

## Workflow

### 1. Check Existing Files

Glob: {all_target_files}

Report what exists vs what will be created.

### 2. Generate {Component 1}

**If no {file1}:**

Invoke the `{plugin}:{skill-1}` skill and follow it exactly.

### 3. Generate {Component 2}

**If no {file2}:**

Invoke the `{plugin}:{skill-2}` skill and follow it exactly.

### 4. Ask About Post-Setup

Present via AskUserQuestion:

{post_setup_options}

### 5. Report Success

============================================================================
{Thing} Environment Ready
============================================================================

Files created:
  ✓ {file1}  - {description}
  ✓ {file2}  - {description}

Commands:
  {usage_commands}
============================================================================
```

## Key Rules

- Always check for existing files before delegating (avoid overwriting)
- Reference other skills by namespaced name: `plugin:skill-name`
- Never link to SKILL.md files directly
- Include `Skill` in allowed-tools
- Orchestrators should be lightweight — the logic lives in the delegated skills
- Report at end summarizes everything that was set up

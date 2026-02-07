# Generator Skill Template

Generator skills detect project context, confirm with user, generate files, and report.

## SKILL.md Template

```yaml
---
name: generating-{thing}
description: Generate {thing} by detecting {context} and applying best practices.
allowed-tools:
  - Read
  - Write
  - Glob
  - AskUserQuestion
---
```

```markdown
# Generate {Thing}

Generate {thing} by detecting {context} and applying best practices.

## Philosophy

- **Detection first** - Scan project before generating
- **User confirmation** - Confirm detected choices
- **Best practices** - Apply conventions from references

## Workflow

### 1. Detect Project Context

Glob: {detection_files}

| File Found | Detected | Reference File |
|------------|----------|----------------|
| {file} | {value} | references/{variant}.md |

### 2. Confirm with User

Present detected choices via AskUserQuestion.

### 3. Load References

Read ONLY the reference files for confirmed choices.

### 4. Generate {Thing}

Compose the file using common sections plus variant content from loaded references.

{ common sections that apply to all variants }

### 5. Report

Created {thing}:

Configuration:
  - {key}: {value}

Commands:
  {usage_commands}

## Reference Files

- references/{variant}.md - {description}
```

## Key Rules

- Common content stays in SKILL.md
- Variant content goes in references, loaded conditionally
- Detection table maps conditions to reference files
- User confirms before generation (AskUserQuestion)
- Report section summarizes what was created

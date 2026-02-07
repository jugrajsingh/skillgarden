# Auditor Skill Template

Auditor skills evaluate existing files against a checklist and report findings with severity.

## SKILL.md Template

```yaml
---
name: auditing
description: Audit {thing} against {standard} best practices and conventions.
allowed-tools:
  - Read
  - Glob
  - Grep
---
```

```markdown
# Audit {Thing}

Evaluate {thing} against best practices.

## Workflow

### 1. Locate Files

Glob: {target_files}

### 2. Detect Context

Determine language/ecosystem to load context-specific checks:

| File Found | Context | Reference File |
|------------|---------|----------------|
| {file} | {context} | references/{context}.md |

### 3. Universal Checks

Checks that apply regardless of context:

| # | Check | Severity | What to Look For |
|---|-------|----------|-----------------|
| 1 | {check_name} | High/Medium/Low | {description} |

### 4. Context-Specific Checks

Read the matching reference file and apply its checks.

### 5. Report

============================================================================
{Thing} Audit Report
============================================================================

Files audited:
  {file_list}

Context: {detected_context}

Findings ({count}):

  {severity} {finding}
  ...

Summary:
  High: {count}  Medium: {count}  Low: {count}
============================================================================

## Reference Files

- references/{context}.md - {context}-specific checks
```

## Severity Levels

| Level | Symbol | Meaning |
|-------|--------|---------|
| High | `◆◆` | Broken or will cause issues |
| Medium | `◆` | Deviation from convention |
| Low | `◇` | Suggestion for improvement |

## Key Rules

- Universal checks in SKILL.md (always evaluated)
- Context-specific checks in references (loaded per detection)
- Every finding has a severity and clear description
- Report groups findings by severity

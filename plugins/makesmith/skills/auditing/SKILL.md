---
name: auditing
description: Use when checking Makefiles for convention violations, missing PHONY declarations, hardcoded paths, or poor role separation between dev and deploy targets
allowed-tools:
  - Read
  - Glob
  - Grep
  - AskUserQuestion
---

# Audit Makefiles

Analyze Makefiles against conventions and best practices.

## Checks

Read `references/universal-checks.md` for the full checklist. Four categories:

1. **Conventions** - .DEFAULT_GOAL, help target, self-documenting, .PHONY, private targets, section separators
2. **Variables** - No hardcoded paths/versions, SCREAMING_SNAKE naming, overridable where needed
3. **Structure** - Role separation (local vs deploy), no mixed concerns, DRY, tag-on-push, root delegates
4. **Best Practices** - Tab indentation, no shell in recipes, quiet prefix, error handling

## Workflow

### 1. Find Makefiles

```text
Glob: Makefile, Makefile.*, */Makefile
```

### 2. Detect Project Language

```text
Glob: pyproject.toml, requirements.txt, uv.lock, package.json, package-lock.json, yarn.lock, pnpm-lock.yaml, go.mod, Cargo.toml
```

Based on detection, load the appropriate language-specific reference:

| Files Found | Reference |
|-------------|-----------|
| `pyproject.toml`, `uv.lock`, `requirements.txt` | `references/python.md` |
| `package.json`, `package-lock.json`, `yarn.lock` | `references/nodejs.md` |

Read the matching reference file for language-specific audit checks. If multiple languages detected, read all matching references.

### 3. Read and Analyze

For each Makefile:

1. Read full content
2. Parse targets (lines matching `^[a-zA-Z_-]+:`)
3. Parse .PHONY declarations
4. Parse variables (lines matching `^[A-Z_]+ :=` or `^[A-Z_]+ \?=`)
5. Check each universal convention
6. Check language-specific conventions from loaded reference

### 4. Cross-File Analysis

- Check role separation between Makefile.local and Makefile.deploy
- Check root Makefile delegates correctly (no inline `uv run`, `npm`, etc.)
- Check consistent variable naming across files

### 5. Generate Report

Use the audit-report.md template. Fill in:

- Each check with (pass), (fail), or (partial)
- Universal findings grouped by category
- Language-specific findings in separate section
- Recommendations sorted by priority

### 6. Ask About Fixes

After presenting the report, ask via AskUserQuestion:

- "Fix all issues" - Apply fixes
- "Fix critical only" - Only fix high-priority items
- "Report only" - No changes

## Priority Classification

| Priority | Criteria |
|----------|----------|
| High | Missing help target, no .PHONY, hardcoded secrets, bare `python`/`node` bypassing package manager |
| Medium | Missing self-documentation, no section separators, DRY violations, missing required targets |
| Low | Naming inconsistencies, missing private prefix on internal targets |

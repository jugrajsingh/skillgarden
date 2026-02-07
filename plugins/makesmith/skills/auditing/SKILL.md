---
name: auditing
description: Audit existing Makefiles against conventions for self-documentation, PHONY declarations, variable usage, and role separation.
allowed-tools:
  - Read
  - Glob
  - Grep
  - AskUserQuestion
---

# Audit Makefiles

Analyze Makefiles against conventions and best practices.

## Checks (Universal)

### Conventions

| Check | Pass Criteria |
|-------|---------------|
| .DEFAULT_GOAL set | `.DEFAULT_GOAL := help` present |
| help target exists | `help:` target with grep/awk pattern |
| Self-documenting | All public targets have `## description` comment |
| .PHONY declarations | All non-file targets listed in .PHONY |
| Private target convention | Internal targets use underscore prefix (_target) or define macros |
| Section separators | Comment blocks separating logical sections |

### Variables

| Check | Pass Criteria |
|-------|---------------|
| No hardcoded paths | Registry URLs, namespaces in variables |
| No hardcoded versions | VERSION derived from git or variable |
| Consistent naming | SCREAMING_SNAKE for variables |
| Overridable where needed | `?=` for KUBE_CONTEXT, NAMESPACE |

### Structure

| Check | Pass Criteria |
|-------|---------------|
| Role separation | Dev targets in Makefile.local, deploy in Makefile.deploy |
| No mixed concerns | Build/push/deploy not mixed with test/lint/format |
| DRY compliance | Repeated docker/helm commands use private targets or define macros |
| Tag-on-push pattern | build-image tags locally, push-image tags for registry |
| Root delegates | Root Makefile delegates to Makefile.local/deploy, no inline commands |

### Best Practices

| Check | Pass Criteria |
|-------|---------------|
| Tab indentation | Recipes use tabs, not spaces |
| No shell assignment in recipe | Use `$(shell ...)` in variables, not in recipes |
| Quiet prefix usage | `@` prefix on echo, not on commands that might fail |
| Error handling | `\|\| true` only on intentional ignore |

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

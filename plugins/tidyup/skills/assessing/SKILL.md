---
name: assessing
description: Use when you need to identify cleanup candidates like dead code, duplication, or staleness before making changes
allowed-tools:
  - Read
  - Glob
  - Grep
  - AskUserQuestion
---

# Codebase Assessment

Read-only analysis of codebase for cleanup candidates. Never modify files during assessment.

## Input

$ARGUMENTS = scope (file path, directory path, or "project").

If empty, ask via AskUserQuestion:

- Options: "Specific file", "Directory", "Entire project", "CLAUDE.md files only"
- If "Specific file" or "Directory": ask for the path

## Step 1: Determine Scope

| Input | Scope |
|-------|-------|
| File path | Single file + cross-references |
| Directory path | All files in directory recursively |
| "project" | Repository root, all tracked files |
| "CLAUDE.md files only" | All CLAUDE.md files in repo |

Identify the repository root via `git rev-parse --show-toplevel`.

## Steps 2-4: Detection

Run dead code detection, duplication scan, and staleness check across all files in scope.

Full detection methods, criteria, and report formats: `references/detection-methods.md`

## Step 5: Context Budget Check

Only if scope includes CLAUDE.md files or scope is "project".

For each CLAUDE.md file found:

```bash
wc -l CLAUDE.md
```

| Lines | Status |
|-------|--------|
| Under 100 | Lean |
| 100-200 | OK |
| Over 200 | Candidate for splitting |

Check for redundancy:

- Compare section headings between root CLAUDE.md and any module-level CLAUDE.md files
- Flag duplicate sections that could be consolidated

## Step 6: Generate Report

Rank all candidates by impact:

| Severity | Meaning |
|----------|---------|
| Severe (two filled diamonds) | Dead code actively confusing or blocking development |
| Major (one filled diamond) | Significant duplication or stale documentation |
| Minor (one empty diamond) | Small unused imports, old TODOs |

Present the full report:

```text
## Assessment: {SCOPE}

### Dead Code ({count} items)
| Severity | File:Line | Type | Description |
|----------|-----------|------|-------------|
| ...      | ...       | ...  | ...         |

### Duplication ({count} items)
| Severity | Location A | Location B | Description |
|----------|------------|------------|-------------|
| ...      | ...        | ...        | ...         |

### Staleness ({count} items)
| Severity | File | Last Modified | Description |
|----------|------|---------------|-------------|
| ...      | ...  | ...           | ...         |

### Context Budget
| File | Lines | Status |
|------|-------|--------|
| ...  | ...   | ...    |

### Summary
- Total candidates: {N}
- Critical: {N} | Major: {N} | Minor: {N}
- Recommended action: /tidyup:cleanup
```

## Rules

- **Read-only** — never modify files during assessment
- Always report file:line for actionable items
- Rank by impact, not by count
- Skip binary files, node_modules, .git, **pycache**, .venv, vendor
- If scope is too large (1000+ files), ask user to narrow down
- Use git-tracked files only (respect .gitignore)

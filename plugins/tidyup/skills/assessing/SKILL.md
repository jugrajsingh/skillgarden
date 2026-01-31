---
name: assessing
description: Analyze codebase for cleanup candidates — dead code, duplication, staleness, context budget
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

## Step 2: Dead Code Detection

For each file in scope:

**Unreferenced functions/classes:**

- Find all function/class definitions (def, class, function, const, export)
- For each definition, search the rest of the codebase for references
- If zero references outside the definition file (excluding tests), flag it
- Exception: entry points (main, **main**, CLI handlers, exports in **init**.py)

**Unused imports:**

- Extract all import statements
- Check if imported name appears elsewhere in the file
- Flag imports where the name is never used after the import line

**Commented-out code:**

- Detect blocks of 3+ consecutive comment lines containing code patterns
- Code patterns: def, class, if, for, while, return, import, from, =, ()
- Single-line comments explaining logic are NOT dead code

Report format per finding: `file:line | type | description`

## Step 3: Duplication Scan

**Function-level duplication:**

- Compare function signatures across files in scope
- Flag functions with identical names and similar parameter counts in different files

**Block-level duplication:**

- Identify code blocks (5+ lines) that appear nearly identical in multiple locations
- "Nearly identical" = same structure, possibly different variable names
- Use grep to find repeated patterns (string literals, logic sequences)

Report format: `fileA:line <-> fileB:line | description`

## Step 4: Staleness Check

**File staleness:**

```bash
git log --oneline -50 --format="%H" | tail -1
```

Use the 50th commit as the cutoff. Find files not modified since:

```bash
git log -1 --format="%ai" -- {FILE}
```

Compare against cutoff commit date.

**Outdated documentation:**

- Find .md files referencing paths or function names that no longer exist
- Check internal links in documentation files

**Old TODOs:**

- Search for TODO, FIXME, HACK comments
- Check git blame for each to determine age
- Flag those older than 20 commits from HEAD

Report format: `file | last modified | description`

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

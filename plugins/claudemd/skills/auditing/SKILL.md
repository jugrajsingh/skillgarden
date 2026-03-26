---
name: auditing
description: Use when checking CLAUDE.md files for anti-patterns, staleness, size budget violations, secrets, or orphaned module files
allowed-tools:
  - Read
  - Glob
  - Grep
  - AskUserQuestion
---

# Audit CLAUDE.md Hierarchy

Analyze ALL context files in the project: root, module-level, and .claude/rules/. Report health issues with severity and actionable fixes.

## Workflow

### 1. Discover All Context Files

Scan the full hierarchy Claude Code autoloads:

```bash
# All CLAUDE.md files (root + module-level)
find . -name 'CLAUDE.md' -not -path '*/node_modules/*' -not -path '*/venv/*' -not -path '*/target/*' -not -path '*/dist/*' 2>/dev/null

# Rules directory
find .claude/rules -name '*.md' -type f 2>/dev/null

# Local file
ls CLAUDE.local.md 2>/dev/null

# Parent directories (monorepo support)
CURRENT="$(pwd)"
while [ "$CURRENT" != "/" ] && [ "$CURRENT" != "$HOME" ]; do
    CURRENT="$(dirname "$CURRENT")"
    ls "$CURRENT/CLAUDE.md" 2>/dev/null
done
```

Classify each file:

| Level | Pattern |
|-------|---------|
| Root | `./CLAUDE.md` or `./.claude/CLAUDE.md` |
| Module | `./src/billing/CLAUDE.md` (subdirectory) |
| Rule | `./.claude/rules/*.md` |
| Local | `./CLAUDE.local.md` |

```text
## Files Discovered

  Level     Path                          Lines  Modified
  Root      ./CLAUDE.md                   {N}    {DATE}
  Module    src/billing/CLAUDE.md         {N}    {DATE}
  Module    src/auth/CLAUDE.md            {N}    {DATE}
  Rule      .claude/rules/testing.md      {N}    {DATE}
  Local     CLAUDE.local.md               {N}    {DATE}
```

If no files found, suggest running `/claudemd:init`.

### 2. Run Audit Checks

Severity indicators:

| Severity | Symbol | Meaning |
|----------|--------|---------|
| Error | ◆◆ | Must fix - actively hurts performance |
| Warning | ◆ | Should fix - wastes context or misleads |
| Info | ◇ | Consider fixing - minor improvement |

Run checks A through G. Read `references/audit-checks.md` for detailed criteria for each check.

- **A: Size Budget** — Compute lines loaded per working directory; flag files exceeding per-level thresholds.
- **B: Content Anti-Patterns** — Flag code style rules, vague instructions, framework basics, and duplicated linter config.
- **C: Secrets and Credentials** — Scan for API keys, connection strings, and tokens.
- **D: Import Integrity** — Verify all @-referenced files exist; flag circular chains and deep imports.
- **E: Module Hierarchy Health** — Detect duplication, orphaned/missing modules, and complementarity violations.
- **F: Staleness Detection** — Compare documented state to actual codebase; use git timestamps as a signal.
- **G: Rule File Quality** — Verify frontmatter, path glob accuracy, cross-cutting scope, and minimum size.

### 3. Generate Report

Read `references/report-template.md` for the full output format.

The report includes: summary counts, health label, per-finding details with actionable fixes, per-file metrics table, context load map, and recommended skill invocations.

## Scoring

```text
Score = 100
  - (errors * 15)
  - (warnings * 5)
  - (info * 1)
  - max(0, (max_loaded - 250) / 5)
```

| Score | Health | Label |
|-------|--------|-------|
| 80-100 | ▓▓▓▓▓ | HEALTHY |
| 50-79 | ▓▓▓░░ | NEEDS_ATTENTION |
| 0-49 | ▓░░░░ | CRITICAL |

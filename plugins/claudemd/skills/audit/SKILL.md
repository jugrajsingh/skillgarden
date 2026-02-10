---
name: audit
description: Analyze health of all CLAUDE.md files - root, module-level, and rules - detecting anti-patterns, staleness, and size issues
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

#### Check A: Size Budget (Per Working Directory)

Budget = max loaded at once, not total across all files.

For each module CLAUDE.md, compute what loads when working there:

```text
Working in src/billing/:
  ./CLAUDE.md              80 lines (always)
  src/billing/CLAUDE.md    55 lines (module)
  .claude/rules/testing.md 20 lines (if path matches)
  = 155 lines loaded
```

| Metric | Target | Warning | Error |
|--------|--------|---------|-------|
| Root CLAUDE.md | 50-80 | >150 | >200 |
| Module CLAUDE.md | 30-50 | >80 | >120 |
| .claude/rules/ file | 15-30 | >50 | >80 |
| Max loaded at once | <150 | >200 | >250 |

#### Check B: Content Anti-Patterns

Search ALL files (root + module + rules) for:

**Code style rules (should use linters):**

- Indentation, quote style, semicolons, line length, import ordering

**Vague instructions (not actionable):**

- "Write clean code", "follow best practices", "be careful with..."

**Framework basics (Claude already knows):**

- Generic React/Vue/Angular patterns, standard HTTP methods, language fundamentals

**Duplicated linter config:**

- Cross-reference with .eslintrc, .prettierrc, ruff.toml, biome.json

#### Check C: Secrets and Credentials

Scan ALL files for:

- API keys: `sk-`, `pk_`, `AKIA`, `ghp_`, `xoxb-`
- Connection strings: `postgres://`, `mongodb://`, `redis://`
- Tokens: `Bearer`, `token=`

#### Check D: Import Integrity

For every `@path/to/file` reference in any context file:

- Verify referenced file exists
- Check for circular import chains
- Warn on imports exceeding 5-hop depth

#### Check E: Module Hierarchy Health

**Duplication between root and modules:**

- Detect content in module files that repeats root CLAUDE.md
- Flag modules that restate root commands, conventions, or tech stack

**Orphaned module files:**

- Module CLAUDE.md exists but directory has <3 source files
- Module CLAUDE.md for a directory that no longer exists

**Missing module files:**

- Directories qualifying under the 4 semantic criteria (Domain Boundary, Integration Point, Sub-App, Technical Complexity) that lack a CLAUDE.md
- Use same judgment logic as `/claudemd:init` Phase 2

**Complementarity violations:**

- Module file that could stand alone (doesn't reference or build on root)
- Module file >80 lines (should split into sub-modules)

#### Check F: Staleness Detection

Compare documented state against actual codebase for ALL files:

**Root staleness:**

- Package versions vs package.json/pyproject.toml
- Directories documented but no longer exist
- Commands that fail when run

**Module staleness:**

- Module references files/components that no longer exist
- Module architecture description doesn't match current code
- Module entry points or interfaces have changed

```bash
# Staleness signal: dependencies changed more recently than context files
git log --format=%ci -1 -- CLAUDE.md 2>/dev/null
find . -name 'CLAUDE.md' -not -path '*/node_modules/*' -exec sh -c 'echo "$(git log --format=%ci -1 -- "$1" 2>/dev/null) $1"' _ {} \;
git log --format=%ci -1 -- package.json pyproject.toml 2>/dev/null
```

#### Check G: Rule File Quality

For each `.claude/rules/*.md`:

- Has YAML frontmatter with `paths:` if path-specific
- Glob patterns match existing paths
- Content is cross-cutting (not module-specific)
- Not duplicating module CLAUDE.md content
- File is >5 lines (otherwise merge elsewhere)

### 3. Generate Report

```text
## CLAUDE.md Audit Report

### Summary

Files scanned: {COUNT} ({ROOT} root, {MODULE} module, {RULE} rules)
Max loaded at once: {MAX}/250 (working in {WORST_PATH})

Health: {HEALTHY | NEEDS_ATTENTION | CRITICAL}

### Findings

◆◆ ERROR: src/billing/CLAUDE.md duplicates root Commands section
   → Remove lines 12-18, root commands already loaded

◆◆ ERROR: Max context load is {N} lines when working in src/billing/stripe/
   → Condense billing module or move content to stripe sub-module

◆ WARNING: Stale root - package.json has react 19, CLAUDE.md says 18
   → Run /claudemd:sync

◆ WARNING: src/legacy/CLAUDE.md - directory has 1 file remaining
   → Remove orphaned module file

◇ INFO: src/middleware/ qualifies as Technical Complexity, no CLAUDE.md
   → Run /claudemd:init src/middleware

### Per-File Metrics

  Path                          Lines  Issues  Status
  ./CLAUDE.md                   {N}    {N}     ✓
  src/billing/CLAUDE.md         {N}    {N}     ◆
  src/auth/CLAUDE.md            {N}    {N}     ✓
  .claude/rules/testing.md      {N}    {N}     ✓

### Context Load Map

Working in...              Files loaded                Total
src/billing/               root + billing              {N}/250
src/billing/stripe/        root + billing + stripe     {N}/250
src/auth/                  root + auth                 {N}/250
(anywhere else)            root only                   {N}/250

### Recommended Actions

1. /claudemd:sync     → Fix {N} stale references
2. /claudemd:optimize → Reduce src/billing/CLAUDE.md from {N} to ~50 lines
3. /claudemd:init src/middleware → Generate missing module file
```

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

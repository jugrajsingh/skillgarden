---
name: optimize
description: Reduce context cost across the full CLAUDE.md hierarchy - condense, deduplicate, and restructure module files
---

# Optimize CLAUDE.md Hierarchy

Reduce context cost across ALL files while preserving signal. Operates on the full hierarchy: root, module-level, and .claude/rules/.

## Optimization Principles

1. **Context is currency** - every line costs tokens when loaded
2. **Signal over prose** - terse directives beat explanatory paragraphs
3. **Complementarity** - modules complement root, never duplicate
4. **Reference over inline** - point to canonical files instead of duplicating
5. **Budget per working directory** - optimize max loaded at once, not total

## Workflow

### 1. Measure Current State

```bash
find . -name 'CLAUDE.md' -not -path '*/node_modules/*' -not -path '*/venv/*' 2>/dev/null | while read f; do echo "$(wc -l < "$f") $f"; done
wc -l .claude/rules/*.md 2>/dev/null
```

Read all files. Compute per-directory load:

```text
## Current Metrics

  Level     Path                          Lines
  Root      ./CLAUDE.md                   {N}
  Module    src/billing/CLAUDE.md         {N}
  Module    src/auth/CLAUDE.md            {N}
  Rule      .claude/rules/testing.md      {N}

Context Load Map:
  Working in...              Loaded                    Total
  src/billing/               root + billing            {N}
  src/auth/                  root + auth               {N}
  (anywhere)                 root only                 {N}

  Worst case: {MAX}/250 (working in {WORST_PATH})
```

If worst-case <100 lines and no anti-patterns: "Hierarchy is already lean. No optimization needed."

### 2. Identify Optimization Opportunities

#### A: Deduplicate Modules Against Root

The highest-value optimization. Module files that repeat root content waste context every time that module is visited.

- Compare each module's sections against root CLAUDE.md
- Flag duplicated commands, conventions, tech stack info
- Module should only contain what's DIFFERENT from root

| Before | After |
|--------|-------|
| Module repeats `npm test` command | Remove — root already documents it |
| Module restates "use TypeScript strict" | Remove — root convention |
| Module adds `npm test -- src/billing/` | Keep — module-specific path |

#### B: Condense Verbose Content

Transform prose into terse directives across ALL files:

**Rules of condensation:**

- Strip filler: "please", "make sure to", "always", "when possible"
- Merge related bullets: single line with separators
- Abbreviate: DB, API, UI, auth, config
- Tables beat paragraphs for structured information

| Before | After |
|--------|-------|
| "When writing tests, always use describe/it and make sure to include meaningful descriptions" | "Tests: describe/it, descriptive names" |
| "The project uses PostgreSQL as the primary database and Redis for caching" | "DB: PostgreSQL. Cache: Redis." |

#### C: Replace Inline Code with References

Across ALL files, replace inline code examples with file pointers:

| Before | After |
|--------|-------|
| 20-line API handler example in module | "API pattern: see src/api/users.ts:15" |
| Test setup boilerplate | "Test setup: follow src/tests/helpers.ts" |

#### D: Remove Linter-Handled Rules

Cross-reference ALL files with detected linter configs:

```bash
ls .editorconfig .eslintrc* .prettierrc* ruff.toml biome.json .flake8 .rubocop.yml 2>/dev/null
```

Remove from ANY context file: indentation, quotes, semicolons, import ordering, line length.

#### E: Restructure Oversized Modules

Module files >80 lines should be split:

- Extract sub-module CLAUDE.md files for child directories
- Push detail down the hierarchy (closer to where it's used)
- Keep parent module as overview + what's unique to its level

```text
# Before: src/billing/CLAUDE.md (120 lines)
  Contains billing overview + stripe details + invoice details

# After:
  src/billing/CLAUDE.md (45 lines) — overview, billing-wide patterns
  src/billing/stripe/CLAUDE.md (35 lines) — stripe integration specifics
  src/billing/invoices/CLAUDE.md (30 lines) — invoice generation specifics
```

#### F: Convert Module Content to Cross-Cutting Rules

If multiple module files contain similar conventions for the same file type, extract to `.claude/rules/`:

```text
# Before: 3 modules each have "use zod for validation"
  src/billing/CLAUDE.md: "Validate with zod schemas"
  src/auth/CLAUDE.md: "All inputs validated with zod"
  src/api/CLAUDE.md: "Use zod for request validation"

# After: one rule file, remove from modules
  .claude/rules/validation.md:
  ---
  paths: ["src/**/*.ts"]
  ---
  Input validation: zod schemas for all request/response types
```

#### G: Remove Orphaned Module Files

Delete CLAUDE.md for directories that:

- No longer exist
- Have <3 source files remaining
- Were consolidated into parent/sibling modules

### 3. Present Plan

```text
## Optimization Plan

Current worst-case load: {N}/250 lines (working in {WORST_PATH})
Target worst-case load: ~{N}/250 lines

### Changes by File

./CLAUDE.md ({N} → ~{N} lines)
  - Condense verbose sections (-{N})
  - Remove linter rules (-{N})

src/billing/CLAUDE.md ({N} → ~{N} lines)
  - Remove duplicated root content (-{N})
  - Extract stripe details to sub-module (-{N})

src/auth/CLAUDE.md ({N} → ~{N} lines)
  - Condense 3 paragraphs to table (-{N})
  - Replace inline example with file ref (-{N})

NEW: src/billing/stripe/CLAUDE.md (~{N} lines)
  - Extracted from oversized billing module

NEW: .claude/rules/validation.md (~{N} lines)
  - Cross-cutting rule extracted from 3 modules

DELETE: src/legacy/CLAUDE.md
  - Directory has 0 source files
```

```yaml
AskUserQuestion:
  question: "Apply this optimization plan?"
  header: "Optimize"
  options:
    - label: "Apply all (Recommended)"
      description: "Execute all optimizations"
    - label: "Cherry-pick"
      description: "Choose which optimizations to apply"
    - label: "Preview only"
      description: "Show proposed file contents without writing"
```

### 4. Apply Optimizations

For each approved optimization:

1. Read the source file
2. Apply the transformation
3. Write the result
4. For new rule files, create with proper YAML frontmatter
5. For new sub-module files, ensure complementarity with parent
6. Verify glob patterns match existing files

### 5. Post-Optimization Report

```text
## Optimization Complete

### Before → After

  Path                          Before  After   Change
  ./CLAUDE.md                   {N}     {N}     -{N}
  src/billing/CLAUDE.md         {N}     {N}     -{N}
  src/billing/stripe/CLAUDE.md  -       {N}     +{N} (extracted)
  src/auth/CLAUDE.md            {N}     {N}     -{N}
  .claude/rules/validation.md   -       {N}     +{N} (cross-cutting)
  src/legacy/CLAUDE.md          {N}     -       removed

### Context Load Map (post-optimization)

Working in...              Before   After
src/billing/               {N}      {N}  (-{SAVED})
src/billing/stripe/        -        {N}  (new path)
src/auth/                  {N}      {N}  (-{SAVED})
(anywhere)                 {N}      {N}  (-{SAVED})

Worst case: {MAX}/250 (was {OLD_MAX})

△ Review with `git diff`. Run /claudemd:audit to validate.
```

## Size Targets

| File Level | Ideal | Max |
|-----------|-------|-----|
| Root CLAUDE.md | 50-80 | 150 |
| Module CLAUDE.md | 30-50 | 80 |
| Sub-module CLAUDE.md | 15-30 | 50 |
| .claude/rules/ file | 15-30 | 50 |
| Max loaded at once | 100-150 | 250 |

# Optimization Categories

## A: Deduplicate Modules Against Root

The highest-value optimization. Module files that repeat root content waste context every time that module is visited.

- Compare each module's sections against root CLAUDE.md
- Flag duplicated commands, conventions, tech stack info
- Module should only contain what's DIFFERENT from root

| Before | After |
|--------|-------|
| Module repeats `npm test` command | Remove — root already documents it |
| Module restates "use TypeScript strict" | Remove — root convention |
| Module adds `npm test -- src/billing/` | Keep — module-specific path |

## B: Condense Verbose Content

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

## C: Replace Inline Code with References

Across ALL files, replace inline code examples with file pointers:

| Before | After |
|--------|-------|
| 20-line API handler example in module | "API pattern: see src/api/users.ts:15" |
| Test setup boilerplate | "Test setup: follow src/tests/helpers.ts" |

## D: Remove Linter-Handled Rules

Cross-reference ALL files with detected linter configs:

```bash
ls .editorconfig .eslintrc* .prettierrc* ruff.toml biome.json .flake8 .rubocop.yml 2>/dev/null
```

Remove from ANY context file: indentation, quotes, semicolons, import ordering, line length.

## E: Restructure Oversized Modules

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

## F: Convert Module Content to Cross-Cutting Rules

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

## G: Remove Orphaned Module Files

Delete CLAUDE.md for directories that:

- No longer exist
- Have <3 source files remaining
- Were consolidated into parent/sibling modules

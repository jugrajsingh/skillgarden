# Audit Checks Reference

## Check A: Size Budget (Per Working Directory)

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

## Check B: Content Anti-Patterns

Search ALL files (root + module + rules) for:

**Code style rules (should use linters):**

- Indentation, quote style, semicolons, line length, import ordering

**Vague instructions (not actionable):**

- "Write clean code", "follow best practices", "be careful with..."

**Framework basics (Claude already knows):**

- Generic React/Vue/Angular patterns, standard HTTP methods, language fundamentals

**Duplicated linter config:**

- Cross-reference with .eslintrc, .prettierrc, ruff.toml, biome.json

## Check C: Secrets and Credentials

Scan ALL files for:

- API keys: `sk-`, `pk_`, `AKIA`, `ghp_`, `xoxb-`
- Connection strings: `postgres://`, `mongodb://`, `redis://`
- Tokens: `Bearer`, `token=`

## Check D: Import Integrity

For every `@path/to/file` reference in any context file:

- Verify referenced file exists
- Check for circular import chains
- Warn on imports exceeding 5-hop depth

## Check E: Module Hierarchy Health

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

## Check F: Staleness Detection

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

## Check G: Rule File Quality

For each `.claude/rules/*.md`:

- Has YAML frontmatter with `paths:` if path-specific
- Glob patterns match existing paths
- Content is cross-cutting (not module-specific)
- Not duplicating module CLAUDE.md content
- File is >5 lines (otherwise merge elsewhere)

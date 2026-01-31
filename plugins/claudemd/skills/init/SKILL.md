---
name: init
description: Generate CLAUDE.md hierarchy - root + module-level files throughout a repository using discovery, judgment, and parallel generation
---

# Init CLAUDE.md Hierarchy

Generate a complete CLAUDE.md hierarchy: root file + module-level files for directories that need local context.

Three phases: **Discovery → Judgment → Generation**.

## Modes

```text
/claudemd:init              # Full repo: all 3 phases
/claudemd:init src/billing  # Single directory: skip to Phase 3
```

If `$ARGUMENTS` contains a path, skip Phase 1 and 2 — generate for that directory only.

## Context Budget Model

Module-level CLAUDE.md files load ON DEMAND. Budget = max loaded at once for any working directory, not total across all files.

```text
~/.claude/CLAUDE.md            always loaded (~personal)
./CLAUDE.md                    always loaded (root)
./.claude/rules/testing.md     loaded when paths: glob matches
./src/billing/CLAUDE.md        loaded when working in src/billing/
```

Working in `src/billing/`: root (80) + billing (50) = 130 lines loaded.

| File Level | Ideal | Max | Loaded |
|-----------|-------|-----|--------|
| Root CLAUDE.md | 50-80 | 150 | Always |
| .claude/rules/ file | 15-30 | 50 | When path matches |
| Module CLAUDE.md | 30-50 | 80 | When working in dir |
| Max loaded at once | 100-150 | 250 | Per working directory |

## Phase 1: Discovery

Build a metadata-rich directory tree from git-tracked files.

### 1a. Check Existing State

```bash
find . -name 'CLAUDE.md' -not -path '*/node_modules/*' -not -path '*/venv/*' 2>/dev/null
ls .claude/rules/*.md 2>/dev/null
```

If root CLAUDE.md exists, ask:

```yaml
AskUserQuestion:
  question: "Existing CLAUDE.md files found. How should I proceed?"
  header: "Existing files"
  options:
    - label: "Regenerate all"
      description: "Fresh analysis, overwrite existing files"
    - label: "Fill gaps"
      description: "Keep existing, generate only for directories missing CLAUDE.md"
    - label: "Cancel"
      description: "Abort without changes"
```

### 1b. Structure Mining

```bash
git ls-files | xargs -n1 dirname | sort | uniq -c | sort -rn
```

For each directory, capture:

| Field | Source |
|-------|--------|
| `path` | Directory path |
| `file_count` | Direct files in this directory |
| `subtree_count` | Total files in subtree |
| `has_manifest` | Contains package.json, go.mod, Cargo.toml, pyproject.toml, Gemfile, pom.xml |
| `has_claude_md` | Already has CLAUDE.md |

```bash
find . -maxdepth 4 \( -name 'package.json' -o -name 'go.mod' -o -name 'Cargo.toml' -o -name 'pyproject.toml' -o -name 'Gemfile' -o -name 'pom.xml' \) -not -path '*/node_modules/*' 2>/dev/null
```

### 1c. Codebase Signals (parallel)

**Tech stack:**

```bash
cat package.json 2>/dev/null | head -30
cat pyproject.toml 2>/dev/null | head -30
cat go.mod 2>/dev/null | head -10
```

**Build/test/lint commands:**

```bash
jq -r '.scripts | keys[]' package.json 2>/dev/null
cat Makefile 2>/dev/null | grep -E '^[a-zA-Z_-]+:' | head -20
```

**Existing conventions:**

```bash
ls .editorconfig .eslintrc* .prettierrc* ruff.toml biome.json .pre-commit-config.yaml 2>/dev/null
```

**Git context:**

```bash
git log --oneline -10
git remote -v 2>/dev/null | head -2
```

### 1d. Semantic Enrichment (Optional)

For directories with 3+ files, read 2-3 representative files and note:

- Exported symbols: class names, function names, type names
- Domain hints from naming (e.g., `AuthService` → auth domain)

Skip if repo is small (<30 files total).

### Discovery Output

```text
## Directory Tree

Path                          Files  Subtree  Manifest  CLAUDE.md
./                            5      142      package   -
src/                          3      120      -         -
src/api/                      5      38       -         -
src/api/handlers/             12     12       -         -
src/billing/                  8      22       package   -
src/auth/                     14     14       -         -
src/utils/                    4      4        -         -
```

## Phase 2: Judgment

Identify which directories warrant their own CLAUDE.md.

**Root always gets a CLAUDE.md.** For all other directories, apply the four semantic criteria.

### Qualification Criteria

A directory qualifies if it matches ANY of:

| Criterion | What to look for |
|-----------|-----------------|
| **Domain Boundary** | Cohesive files forming a distinct conceptual area. Someone would work "in this domain." Examples: auth, billing, search |
| **Integration Point** | Connects to external systems. Filenames suggest: webhook, client, adapter, provider, gateway |
| **Sub-App** | Self-contained with entry points, routes, or own runtime. Could be extracted as standalone |
| **Technical Complexity** | Non-obvious patterns an agent would get wrong without local guidance |

### Two Critical Rules

#### Rule 1: Children Over Parent

When parent qualifies, check if children also qualify. If children qualify, generate for EACH child and SKIP the parent.

```text
src/api/           → SKIP (children cover it)
src/api/handlers/  → ✓ Integration point
src/api/middleware/ → ✓ Technical complexity
```

#### Rule 2: Semantic Citation

Cite which criterion applies for each target. No "other" category. If none apply, the directory does not need a CLAUDE.md.

### Exclusion Signals

Skip directories that are:

- Pure utility/helper collections (string utils, math helpers)
- Auto-generated code directories
- Test directories that mirror source structure
- Vendor/dependency directories
- Directories with <3 files and no manifest

### Judgment Output

```text
## Targets

  #  Path                    Criterion
  0  ./                      Root (always)
  1  src/api/handlers/       Integration point
  2  src/billing/            Domain boundary
  3  src/billing/stripe/     Integration point
  4  src/auth/               Domain boundary

Skipped:
- src/utils/ (utility collection)
- src/api/ (children cover it)
```

```yaml
AskUserQuestion:
  question: "Generate CLAUDE.md for these directories?"
  header: "Targets"
  options:
    - label: "All targets (Recommended)"
      description: "Generate root + {N} module files"
    - label: "Select targets"
      description: "Choose which directories to include"
    - label: "Root only"
      description: "Generate only root CLAUDE.md"
```

## Phase 3: Generation

### 3a. Generate Root CLAUDE.md

Use the WHAT-WHY-HOW framework. Each section earns its place.

```markdown
# {PROJECT_NAME}

{ one-line purpose }

## Tech Stack

{ only non-obvious versions/tools }

## Structure

{ key directories with 2-3 word purpose annotations }
{ only directories Claude needs to navigate }

## Commands

{ build, test, lint with exact syntax }
{ skip obvious ones like `npm install` }

## Conventions

{ project-specific patterns and anti-patterns }
{ not language/framework defaults }

## Gotchas

{ things that break, workarounds, non-obvious behavior }
```

**Omit a section if it would only state the obvious.**

Section inclusion:

| Section | Include when... |
|---------|----------------|
| Tech Stack | Non-obvious versions, custom tooling |
| Structure | >5 directories with distinct purposes |
| Commands | Build/test commands aren't self-evident |
| Conventions | Project deviates from framework defaults |
| Gotchas | Known pitfalls exist |

### 3b. Generate Module CLAUDE.md Files (Parallel)

Read the root CLAUDE.md first. All subagents need this context.

For each target, spawn a `Task(general-purpose)` subagent:

```text
Task for {target.path}:

CONTEXT: The root CLAUDE.md contains:
---
{root_claude_md_content}
---

Create {target.path}/CLAUDE.md. This file autoloads when Claude works
in {target.path}/. It COMPLEMENTS the root (always loaded). Never
repeat what root covers.

INCLUDE:

1. Module purpose - one line: what this directory is and does
2. Architecture - how components relate (big picture requiring
   multiple files to understand)
3. Local commands - subdirectory-specific test/build paths or flags
4. Conventions - patterns unique to THIS directory
5. Gotchas - non-obvious behavior, pitfalls, workarounds
6. Key interfaces - entry points, public API surface

EXCLUDE:

- Anything the root CLAUDE.md covers
- Generic practices ("write tests", "handle errors")
- Exhaustive file listings (discoverable via ls)
- Framework patterns Claude already knows
- Made-up sections with no real content
- Code style rules handled by linters

CONSTRAINTS:

- Under 80 lines
- No section with fewer than 2 actionable items
- Reference canonical files instead of inline code examples
- If CLAUDE.md exists, suggest improvements vs creating new
```

**Dispatch all subagents in a single message for parallel execution.**

### 3c. Generate Cross-Cutting Rules (Optional)

If the codebase has conventions that span multiple modules but only apply to specific file types, create `.claude/rules/` files:

```markdown
---
paths:
  - "**/*.test.{ts,py}"
---

# Test Conventions

{ rules that apply to ALL test files across modules }
```

Use `.claude/rules/` ONLY for cross-cutting concerns. Module-specific content goes in module CLAUDE.md.

| Mechanism | When to use |
|-----------|-------------|
| Module CLAUDE.md | Domain-specific: architecture, local patterns, integration contracts |
| .claude/rules/ | Cross-cutting: test conventions, API style, security rules across all modules |

### 3d. Generate CLAUDE.local.md Template

```bash
grep -q 'CLAUDE.local.md' .gitignore 2>/dev/null || echo "CLAUDE.local.md" >> .gitignore
```

### 3e. Post-Generation Validation

For each generated file:

- [ ] Within size target for its level
- [ ] No duplication with root CLAUDE.md
- [ ] No secrets, credentials, or API keys
- [ ] No code style rules that linters handle
- [ ] No framework basics Claude already knows
- [ ] No section with fewer than 2 actionable items

## Summary Report

```text
## Init Complete

### Files Generated

  Path                            Lines  Level        Criterion
✓ ./CLAUDE.md                     {N}    Root         -
✓ src/api/handlers/CLAUDE.md      {N}    Module       Integration point
✓ src/billing/CLAUDE.md           {N}    Module       Domain boundary
✓ src/billing/stripe/CLAUDE.md    {N}    Sub-module   Integration point
✓ src/auth/CLAUDE.md              {N}    Module       Domain boundary
✓ .claude/rules/testing.md        {N}    Rule         Cross-cutting
  CLAUDE.local.md                 {N}    Local        Personal (gitignored)

### Context Budget (per working directory)

Working in...              Loaded files               Total lines
src/billing/               root + billing             {N}
src/billing/stripe/        root + billing + stripe    {N}
src/auth/                  root + auth                {N}
(anywhere else)            root only                  {N}

Max loaded at once: {MAX}/250

### Next Steps

- Review: git diff
- Validate: /claudemd:audit
- Re-generate one dir: /claudemd:init {path}
```

## Anti-Patterns

| Anti-Pattern | Why |
|-------------|-----|
| Copying README into CLAUDE.md | Duplicates info, wastes context |
| "Use clean code practices" | Vague, Claude already does this |
| Documenting every directory | Only document non-obvious structure |
| Style rules like "use 2-space indent" | Use .editorconfig or formatters |
| Repeating root content in module files | Modules complement, never duplicate |
| Module file >80 lines | Too broad, split into sub-modules |

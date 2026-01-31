---
name: sync
description: Update all CLAUDE.md files to reflect current codebase - fix drift in root, module, and rule files
---

# Sync CLAUDE.md Hierarchy

Detect drift between documented context and actual codebase state across ALL files: root, module-level, and .claude/rules/. Apply surgical updates.

## Workflow

### 1. Discover All Context Files

```bash
find . -name 'CLAUDE.md' -not -path '*/node_modules/*' -not -path '*/venv/*' -not -path '*/target/*' -not -path '*/dist/*' 2>/dev/null
find .claude/rules -name '*.md' -type f 2>/dev/null
```

Classify each as Root, Module, or Rule (same as audit).

If no files found: "No context files to sync. Run `/claudemd:init` first."

### 2. Read Current State

Read all discovered files. For each file, note:

- Level (root/module/rule)
- Sections and their content
- References to specific versions, paths, commands, files

### 3. Analyze Codebase (Current Truth)

Run these in parallel:

**a) Tech stack:**

```bash
cat package.json 2>/dev/null | jq '{name, dependencies, devDependencies}' 2>/dev/null
cat pyproject.toml 2>/dev/null
cat go.mod 2>/dev/null | head -20
cat Cargo.toml 2>/dev/null | head -30
```

**b) Directory structure:**

```bash
git ls-files | xargs -n1 dirname | sort -u
```

**c) Available commands:**

```bash
jq -r '.scripts | to_entries[] | "\(.key): \(.value)"' package.json 2>/dev/null
cat Makefile 2>/dev/null | grep -E '^[a-zA-Z_-]+:' 2>/dev/null
```

**d) Linter/formatter config:**

```bash
ls .editorconfig .eslintrc* .prettierrc* ruff.toml biome.json .flake8 .rubocop.yml 2>/dev/null
```

**e) Module-level changes:**

For each module CLAUDE.md, check its directory:

```bash
# Files in module directory vs what module documents
find {module_path} -maxdepth 1 -type f | head -30
```

**f) Staleness signals:**

```bash
# For each context file, compare its last commit to codebase changes
find . -name 'CLAUDE.md' -not -path '*/node_modules/*' -exec sh -c 'echo "$(git log --format=%ci -1 -- "$1" 2>/dev/null) $1"' _ {} \;
git log --format=%ci -1 -- package.json pyproject.toml Makefile 2>/dev/null
```

### 4. Compute Diff (Per File)

For EACH context file, compare documented state vs reality:

**Root drift dimensions:**

| Dimension | Source of Truth | Documented In |
|-----------|----------------|---------------|
| Dependencies | package.json / pyproject.toml | Tech Stack section |
| Directories | Filesystem + git ls-files | Structure section |
| Commands | package.json scripts / Makefile | Commands section |

**Module drift dimensions:**

| Dimension | Source of Truth | Documented In |
|-----------|----------------|---------------|
| Module files | Filesystem | Architecture / structure references |
| Entry points | Source code exports | Key interfaces section |
| Local commands | Package scripts / Makefile targets | Commands section |

**Rule drift dimensions:**

| Dimension | Source of Truth | Documented In |
|-----------|----------------|---------------|
| Path globs | Filesystem | YAML frontmatter `paths:` |
| Cross-cutting conventions | Codebase patterns | Rule content |

Change classification:

| Symbol | Meaning |
|--------|---------|
| + | New in codebase, not documented |
| - | Documented but no longer exists |
| ~ | Changed (version, path, name) |

### 5. Present Changes

```text
## Sync Report

### Root CLAUDE.md

~ react: 18.2.0 → 19.1.0 (line 8)
+ vitest: 3.1.0 (new, not documented)
- jest: removed from deps (line 12)
~ test command: "jest" → "vitest run" (line 22)

### Module: src/billing/CLAUDE.md

- src/billing/legacy.py referenced but deleted
+ src/billing/v2/ new subdirectory, not documented
~ entry point changed: BillingService → BillingV2Service

### Module: src/auth/CLAUDE.md

= No drift detected

### Rule: .claude/rules/api.md

~ paths glob "src/api/**" matches 0 files (directory renamed to src/endpoints/)

### Hierarchy Changes

+ src/notifications/ qualifies as Domain Boundary, no CLAUDE.md
- src/legacy/CLAUDE.md orphaned (directory has 0 source files)
```

### 6. Ask User

```yaml
AskUserQuestion:
  question: "How should I apply these changes?"
  header: "Apply"
  options:
    - label: "Apply all (Recommended)"
      description: "Update all drifted files automatically"
    - label: "Review each"
      description: "Step through each file for approval"
    - label: "Preview only"
      description: "Show proposed edits without applying"
```

### 7. Apply Updates

For each approved change:

- Edit specific lines in the affected file
- Preserve surrounding context and formatting
- Keep within size budgets per level
- For orphaned module files: ask before deleting
- For new qualifying directories: suggest `/claudemd:init {path}`

### 8. Post-Sync Report

```text
## Sync Complete

### Updated Files

  Path                          Changes  Lines before → after
  ./CLAUDE.md                   3        82 → 80
  src/billing/CLAUDE.md         2        55 → 48
  .claude/rules/api.md          1        25 → 25

### Unresolved

+ src/notifications/ needs CLAUDE.md → /claudemd:init src/notifications
- src/legacy/CLAUDE.md orphaned → delete manually or /claudemd:optimize

### Context Load (post-sync)

Working in...              Total loaded
src/billing/               root (80) + billing (48) = 128/250

△ Review changes with `git diff` before committing.
```

## What Sync Does

- Updates facts: versions, paths, commands, file references
- Flags orphaned module files
- Flags new directories that qualify for CLAUDE.md
- Updates stale path globs in rule frontmatter

## What Sync Does NOT Do

- Does not restructure files (use `/claudemd:optimize`)
- Does not generate new module files (use `/claudemd:init {path}`)
- Does not rewrite prose or change writing style
- Does not touch CLAUDE.local.md (personal file)
- Does not delete files without explicit user approval

Sync is surgical: facts only, no restructuring.

---
name: syncing
description: Use when CLAUDE.md files may be outdated — package versions changed, directories renamed, commands modified, or modules reference deleted files
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
  - AskUserQuestion
---

# Sync CLAUDE.md Hierarchy

Detect drift between documented context and actual codebase state across ALL files: root, module-level, and .claude/rules/. Apply surgical updates.

## Workflow

### 1. Discover All Context Files

```bash
find . -name 'CLAUDE.md' -not -path '*/node_modules/*' -not -path '*/venv/*' -not -path '*/target/*' -not -path '*/dist/*' 2>/dev/null
find .claude/rules -name '*.md' -type f 2>/dev/null
```

Classify each as Root, Module, or Rule. If no files found: "No context files to sync. Run `/claudemd:init` first."

### 2. Read Current State

Read all discovered files. For each file, note: level (root/module/rule), sections and their content, references to specific versions, paths, commands, and files.

### 3. Analyze Codebase (Current Truth)

Run tech stack, directory structure, available commands, linter config, module-level, and staleness signal checks in parallel. See `references/drift-analysis.md` for all bash commands.

### 4. Compute Diff (Per File)

Compare documented state vs reality across root, module, and rule drift dimensions. Classify each change as + (new), - (removed), or ~ (changed). See `references/drift-analysis.md` for dimension tables and classification symbols.

### 5. Present Changes

Show a sync report grouped by file, listing each drift item with symbol, description, and line reference. See `references/report-templates.md` for the full report format.

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

For each approved change: edit specific lines in the affected file, preserve surrounding context and formatting, keep within size budgets per level. For orphaned module files: ask before deleting. For new qualifying directories: suggest `/claudemd:init {path}`.

### 8. Post-Sync Report

Show updated files with change counts and line deltas, list unresolved items with suggested commands, and display context load totals per working directory. See `references/report-templates.md` for the full report format.

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

---
name: optimizing
description: Use when CLAUDE.md files are too large, have duplicated content between root and modules, or the context budget per working directory exceeds limits
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
  - AskUserQuestion
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

Read all files. Compute per-directory context load (root + all modules loaded for that working directory). If worst-case <100 lines and no anti-patterns: "Hierarchy is already lean. No optimization needed."

### 2. Identify Optimization Opportunities

Apply the 7 categories from `references/optimizations.md`:

- **A: Deduplicate Modules** — remove module content that repeats root
- **B: Condense Verbose Content** — strip filler, merge bullets, use tables
- **C: Replace Inline Code** — swap examples for file references
- **D: Remove Linter-Handled Rules** — check linter configs, purge redundant rules
- **E: Restructure Oversized Modules** — split modules >80 lines into sub-modules
- **F: Cross-Cutting Rules** — extract repeated conventions to .claude/rules/
- **G: Remove Orphaned Files** — delete CLAUDE.md for defunct directories

Full descriptions, before/after examples, and code blocks for each category are in `references/optimizations.md`.

### 3. Present Plan

Show the current worst-case load, target load, and per-file change summary. Use the plan template from `references/report-templates.md`.

Ask user to confirm before applying: "Apply all", "Cherry-pick", or "Preview only".

### 4. Apply Optimizations

For each approved optimization:

1. Read the source file
2. Apply the transformation
3. Write the result
4. For new rule files, create with proper YAML frontmatter
5. For new sub-module files, ensure complementarity with parent
6. Verify glob patterns match existing files

### 5. Post-Optimization Report

Show before/after line counts per file and updated context load map. Use the report template from `references/report-templates.md`.

## Size Targets

| File Level | Ideal | Max |
|-----------|-------|-----|
| Root CLAUDE.md | 50-80 | 150 |
| Module CLAUDE.md | 30-50 | 80 |
| Sub-module CLAUDE.md | 15-30 | 50 |
| .claude/rules/ file | 15-30 | 50 |
| Max loaded at once | 100-150 | 250 |

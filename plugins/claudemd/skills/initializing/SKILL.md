---
name: initializing
description: Use when a repository needs CLAUDE.md files generated from scratch, or when a new directory needs its own module-level context file
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Task
  - AskUserQuestion
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

Build a metadata-rich directory tree from git-tracked files. Check existing CLAUDE.md files, mine directory structure, collect tech stack and build commands, and optionally enrich with semantic signals from representative files.

Full steps, bash commands, and output format: `references/discovery-phase.md`

## Phase 2: Judgment

Identify which directories warrant their own CLAUDE.md. Root always qualifies. Apply four criteria to all others: Domain Boundary, Integration Point, Sub-App, Technical Complexity. Prefer children over parents when both qualify. Present targets to user for confirmation before generating.

Full criteria, exclusion signals, and output format: `references/judgment-phase.md`

## Phase 3: Generation

Generate root CLAUDE.md using WHAT-WHY-HOW framework, then dispatch all module files as parallel subagents. Optionally generate `.claude/rules/` for cross-cutting conventions and a gitignored `CLAUDE.local.md` template. Validate each file post-generation.

Full instructions, subagent dispatch format, and validation checklist: `references/generation-phase.md`

After generation, output the summary report. Template: `references/report-template.md`

## Anti-Patterns

| Anti-Pattern | Why |
|-------------|-----|
| Copying README into CLAUDE.md | Duplicates info, wastes context |
| "Use clean code practices" | Vague, Claude already does this |
| Documenting every directory | Only document non-obvious structure |
| Style rules like "use 2-space indent" | Use .editorconfig or formatters |
| Repeating root content in module files | Modules complement, never duplicate |
| Module file >80 lines | Too broad, split into sub-modules |

---
name: cleaning-up
description: Use when you have identified cleanup candidates and are ready to safely remove dead code, consolidate duplicates, and archive stale files
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(git *)
  - Skill
  - AskUserQuestion
---

# Cleanup Workflow

Execute codebase cleanup with mandatory safety gates. Zero information loss — archive, never delete.

## Input

$ARGUMENTS = scope or path to previous assessment output.

If empty, ask via AskUserQuestion:

- Options: "Run full assessment first", "Use existing assessment", "Quick cleanup (single file)"
- If "Quick cleanup": ask for the file path
- If "Use existing assessment": ask user to paste or reference the assessment

## Phase 1: Assessment

**If no assessment exists:**

- Load the `tidyup:assessing` skill to generate one
- Wait for assessment to complete before proceeding

**If assessment provided:**

- Parse the assessment report
- Verify currency: check that referenced files still exist and haven't been modified since assessment
- If files changed since assessment, warn user and offer to re-assess

## Phase 2: Present Cleanup Plan

Group candidates by action type:

| Action | Applies To |
|--------|-----------|
| Remove | Dead code (unused imports, unreferenced functions, commented-out code) |
| Consolidate | Duplicate code blocks |
| Archive | Stale documentation, obsolete files |

Present each candidate via AskUserQuestion with multiSelect: true.

Format each option as: `[severity] action: file:line — description`

Example options:

- `[major] Remove: src/utils.py:45 — unreferenced function parse_legacy()`
- `[minor] Remove: src/api.py:3 — unused import os`
- `[major] Consolidate: src/a.py:20 + src/b.py:30 — duplicate validation logic`
- `[minor] Archive: docs/old-api.md — not modified in 80 commits`

CRITICAL: Never auto-execute cleanup. Always get explicit user approval for every item.

## Phase 3: Remove Dead Code

Remove unused imports, unreferenced functions/classes, and commented-out code. Verify with grep after each removal — revert if references found.

## Phase 4: Consolidate Duplicates

Identify canonical location (prefer more complete, closer to shared/utils, or older). Extract to shared utility, update all call sites.

## Phase 5: Archive Stale Content

CRITICAL: Never delete files. Always archive to `.archive/` with mirrored directory structure. Update `.archive/MANIFEST.md`.

Full step-by-step procedures for phases 3-5: `references/cleanup-phases.md`

## Phase 6: Verify

Run detected test suite, revert any change that causes failures, and generate cleanup report.

Full verification procedure, test runner detection, and report template: `references/verification.md`

## Rules

- NEVER delete without archiving — zero information loss
- ALWAYS run tests after changes
- ALWAYS get explicit user approval before any modification
- If tests fail after a change, revert that specific change and continue
- One change at a time — do not batch removals in a single edit
- Keep a running log of all actions for the final report
- Skip binary files, generated files, and vendored dependencies
- Respect .gitignore — never touch ignored files
- If unsure whether something is dead code, ask the user rather than removing it

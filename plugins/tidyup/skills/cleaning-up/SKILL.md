---
name: cleaning-up
description: Execute codebase cleanup with safety gates — assess, confirm, remove, consolidate, archive, verify
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

For each approved removal, execute in order:

### Unused Imports

1. Read the file
2. Remove the import line(s)
3. If import was part of a grouped import (e.g., `from x import a, b, c`), remove only the unused name
4. Verify: grep the file for the removed name to confirm it's truly unused

### Unreferenced Functions/Classes

1. Read the file
2. Identify the full extent of the function/class (definition through last line)
3. Remove the entire definition including decorators and docstring
4. Verify: grep the codebase for the function/class name
5. If any reference found outside the original location, STOP and report to user

### Commented-Out Code

1. Read the file
2. Remove the consecutive comment block identified in assessment
3. Preserve any non-code comments (explanatory text) adjacent to the block

After each removal:

```bash
# Sanity check — search for broken references
grep -r "removed_name" --include="*.py" --include="*.ts" --include="*.js" .
```

If references found, revert the change and report to user.

## Phase 4: Consolidate Duplicates

For each approved consolidation:

### Identify Canonical Location

Decision criteria:

- Prefer the more complete implementation
- Prefer the file closer to shared/utils in the directory tree
- If equal, prefer the older version (first committed)

### Extract and Deduplicate

1. Read both files containing duplicate code
2. Choose canonical location
3. If both files import from the same parent module:
   - Extract to a shared utility in the common parent
   - Update both files to import from the shared location
4. If files are in different modules:
   - Keep the version in the more appropriate location
   - Replace the other with an import/reference to the canonical version
5. Update all call sites across the codebase

After each consolidation:

```bash
# Verify all references resolve
grep -rn "function_name" --include="*.py" --include="*.ts" --include="*.js" .
```

## Phase 5: Archive Stale Content

CRITICAL: Never delete files. Always archive.

### Setup Archive Directory

```bash
mkdir -p .archive
```

If .archive is not in .gitignore, warn the user and suggest adding it.

### Archive Process

For each approved archive:

1. Create the mirrored directory structure:

   ```bash
   mkdir -p .archive/{original-directory-path}
   ```

2. Move the file:

   ```bash
   git mv {original-path} .archive/{original-path}
   ```

   If not git-tracked, use regular mv.

3. Update references:
   - Search for any imports, links, or references to the archived file
   - Update or annotate them with the new archive location
   - If a reference is in active code (not docs), warn user instead of auto-updating

### Archive Manifest

After all archives, create or update `.archive/MANIFEST.md`:

```text
# Archive Manifest

| Original Path | Archived Date | Reason |
|---------------|---------------|--------|
| docs/old-api.md | {DATE} | Stale — not modified in 80 commits |
```

## Phase 6: Verify

### Run Test Suite

Detect the test runner from project configuration:

| File | Runner | Command |
|------|--------|---------|
| pytest.ini / pyproject.toml (pytest) | pytest | `pytest` |
| package.json | npm/yarn | `npm test` |
| Cargo.toml | cargo | `cargo test` |
| go.mod | go | `go test ./...` |
| Makefile (test target) | make | `make test` |

Run the detected test suite:

```bash
{TEST_COMMAND}
```

### Handle Test Failures

If tests fail after a change:

1. Identify which cleanup action caused the failure
2. Revert that specific change (re-read file from git):

   ```bash
   git checkout -- {FILE}
   ```

3. Report the failure to user with details
4. Continue with remaining cleanup items

### Generate Cleanup Report

Use the template from `templates/cleanup-report.md` as the structure.

Fill in all sections:

```text
## Cleanup Report: {SCOPE}

### Actions Taken
| Action | File | Type | Details |
|--------|------|------|---------|
| Removed | path:line | dead code | {description} |
| Consolidated | pathA + pathB | duplication | {description} |
| Archived | path -> .archive/path | stale | {description} |

### Metrics
- Lines removed: {N}
- Files archived: {N}
- Duplicates consolidated: {N}

### Test Results
- Suite: {runner}
- Status: {pass/fail}
- Tests: {passed}/{total}

### Verification
- All references intact
- Tests passing
- No information lost (archived, not deleted)
```

If any verification item fails, mark it and explain.

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

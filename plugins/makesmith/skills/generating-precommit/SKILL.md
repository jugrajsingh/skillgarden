---
name: generating-precommit
description: Generate pre-commit hooks for Makefile linting with mbake
allowed-tools:
  - Read
  - Write
  - Glob
  - AskUserQuestion
---

# Makefile Pre-commit Hooks

Add Makefile linting to pre-commit configuration using mbake.

## Tool: mbake

mbake is a Makefile formatter and linter.

```bash
pip install mbake
mbake format --check Makefile
```

## Workflow

### 1. Check for Makefiles

```text
Glob: Makefile, */Makefile, **/Makefile
```

If no Makefiles found, report and exit.

### 2. Check Existing Pre-commit Config

```text
Glob: .pre-commit-config.yaml
```

If exists, merge mbake hook. If not, create minimal config.

### 3. Add mbake Hook

Use a local hook since mbake doesn't have an official pre-commit repo:

```yaml
  # Makefile linting
  - repo: local
    hooks:
      - id: mbake
        name: mbake format
        entry: mbake format --check
        language: python
        additional_dependencies:
          - mbake
        files: (^|/)Makefile$
        types:
          - file
```

### 4. Report

```text
Added Makefile linting to pre-commit:

Hook: mbake (local)
Files: Makefile, */Makefile

Install mbake: pip install mbake

Commands:
  mbake format Makefile        # Format in place
  mbake format --check Makefile  # Check only (CI mode)
```

## mbake Features

- **Format**: Consistent indentation and spacing
- **Check**: Validate formatting without changes
- **Diff**: Show what would change

## Hook Behavior

- Runs only when Makefile changes
- Skips if no Makefile present
- Uses `--check` flag (fails if formatting needed)

## Manual Fix

If hook fails:

```bash
mbake format Makefile
git add Makefile
```

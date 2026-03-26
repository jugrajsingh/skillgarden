---
name: setting-up
description: Use when bootstrapping a new Python project from scratch or when a project needs pyproject.toml, settings, pre-commit, and Makefile in one pass
allowed-tools:
  - Read
  - Glob
  - Bash(uv *)
  - Bash(make *)
  - Bash(pre-commit *)
  - Bash(which *)
  - Bash(pwd)
  - Bash(basename *)
  - Skill
  - AskUserQuestion
---

# Python Local Environment Setup (Orchestrator)

Orchestrates complete Python dev environment setup by invoking specialized generator skills.

## What Gets Set Up

1. **pyproject.toml** - Dependencies + tool configs (uv-native)
2. **config/settings.py** - Pydantic Settings + example.env.yaml
3. **.pre-commit-config.yaml** - Security + quality hooks
4. **Makefile.local** - Dev commands with configured venv location
5. **CLAUDE.md Commands section** - Agent instructions for Makefile usage (via makesmith)
6. **Virtual environment** - Created via Makefile.local

## Prerequisites

- **uv** must be installed: `curl -LsSf https://astral.sh/uv/install.sh | sh`

## Workflow

### 1. Verify uv is Available

```bash
which uv
```

If not found, instruct user to install uv first.

### 2. Check Existing Files

```text
Glob: pyproject.toml, config/settings.py, .pre-commit-config.yaml, Makefile.local
```

Report what exists vs what will be created.

### 3. Generate Files (invoke skills in order)

For each missing file, invoke the corresponding skill:

| File | Condition | Skill to Invoke |
|------|-----------|-----------------|
| pyproject.toml | Missing | `pysmith:generating-pyproject` |
| config/settings.py | Missing | `pysmith:generating-settings` |
| .pre-commit-config.yaml | Missing | `pysmith:generating-precommit` |
| Makefile.local | Missing | `makesmith:generating-local` |

Each skill handles its own user interactions (merge vs overwrite, section selection, etc.).

### 4. Execute Setup

After all configs are generated, run the setup via Makefile.local:

```bash
make -f Makefile.local setup-local
```

This executes:

1. `create-venv` - Creates venv at configured location
2. `install-dev` - Runs `uv sync` to install all dependencies
3. `install-hooks` - Runs `pre-commit install`

### 5. Report Success

```text
============================================================================
Python Local Environment Ready
============================================================================

Files created/updated:
  ✓ pyproject.toml           - Dependencies + tool configs
  ✓ config/settings.py       - Pydantic Settings
  ✓ example.env.yaml         - Configuration template
  ✓ .pre-commit-config.yaml  - Pre-commit hooks
  ✓ Makefile.local           - Dev commands
  ✓ CLAUDE.md (Commands)     - Agent instructions updated

Virtual environment:
  Location: {venv_location}
  Python:   {python_version}

Next steps:
  1. cp example.env.yaml local.env.yaml
  2. Edit local.env.yaml with your settings
  3. make -f Makefile.local test

Common commands:
  make -f Makefile.local help        # Show all targets
  make -f Makefile.local test        # Run all tests
  make -f Makefile.local test-unit   # Unit tests only
  make -f Makefile.local lint        # Check code
  make -f Makefile.local format      # Format code
  make -f Makefile.local quality     # All quality checks
  make -f Makefile.local pre-commit  # Run pre-commit hooks

IMPORTANT: Always use Makefile targets, never raw uv/python commands.
============================================================================
```

## Partial Setup

If some files already exist, the orchestrator:

- Skips generation for existing files (unless user chooses to overwrite)
- Still runs `make -f Makefile.local setup-local` to ensure venv is ready

## Error Handling

**If uv not installed:**

```text
Error: uv is not installed.

Install uv:
  curl -LsSf https://astral.sh/uv/install.sh | sh

Or see: https://docs.astral.sh/uv/getting-started/installation/
```

**If generator skill fails:**

- Report which skill failed
- Suggest running it directly for more details
- Continue with remaining skills if possible

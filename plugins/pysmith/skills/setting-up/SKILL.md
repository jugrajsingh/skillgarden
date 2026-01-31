---
name: setting-up
description: Orchestrate complete Python dev environment setup by invoking specialized generator skills. Creates pyproject.toml, config/settings.py, .pre-commit-config.yaml, and Makefile.local.
allowed-tools:
  - Read
  - Glob
  - Bash(uv *)
  - Bash(make *)
  - Bash(pre-commit *)
  - Bash(which *)
  - Bash(pwd)
  - Bash(basename *)
  - AskUserQuestion
  - Skill
---

# Python Local Environment Setup (Orchestrator)

Orchestrates complete Python dev environment setup by invoking specialized generator skills.

## What Gets Set Up

1. **pyproject.toml** - Dependencies + tool configs (uv-native)
2. **config/settings.py** - Pydantic Settings + example.env.yaml
3. **.pre-commit-config.yaml** - Security + quality hooks
4. **Makefile.local** - Dev commands with configured venv location
5. **Virtual environment** - Created via Makefile.local

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

### 3. Generate pyproject.toml

**If no pyproject.toml:**

Invoke the `pysmith:generating-pyproject` skill and follow it exactly.

This generates:

- `[project]` with dependencies
- `[dependency-groups]` with dev deps
- `[tool.*]` configurations for ruff, pytest, mypy, coverage

### 4. Generate Pydantic Settings

**If no config/settings.py:**

Invoke the `pysmith:generating-settings` skill and follow it exactly.

This generates:

- `config/settings.py` - Settings class with selected sections
- `example.env.yaml` - Configuration template
- Updates `.gitignore` for *.env.yaml

### 5. Generate Pre-commit Config

**If no .pre-commit-config.yaml:**

Invoke the `pysmith:generating-precommit` skill and follow it exactly.

This generates:

- `.pre-commit-config.yaml` with gitleaks, pip-audit, ruff hooks

### 6. Generate Makefile.local

**If no Makefile.local:**

Invoke the `makesmith:generating-local` skill and follow it exactly.

This:

- Asks user for venv location preference
- Generates `Makefile.local` with all dev commands
- Configures `UV_PROJECT_ENVIRONMENT` for chosen venv location

### 7. Execute Setup

After all configs are generated, run the setup via Makefile.local:

```bash
make -f Makefile.local setup-local
```

This executes:

1. `create-venv` - Creates venv at configured location
2. `install-dev` - Runs `uv sync` to install all dependencies
3. `install-hooks` - Runs `pre-commit install`

### 8. Report Success

```text
============================================================================
Python Local Environment Ready
============================================================================

Files created/updated:
  ✓ pyproject.toml      - Dependencies + tool configs
  ✓ config/settings.py  - Pydantic Settings
  ✓ example.env.yaml    - Configuration template
  ✓ .pre-commit-config.yaml - Pre-commit hooks
  ✓ Makefile.local      - Dev commands

Virtual environment:
  Location: {venv_location}
  Python:   {python_version}

Next steps:
  1. cp example.env.yaml local.env.yaml
  2. Edit local.env.yaml with your settings
  3. make -f Makefile.local test

Common commands:
  make -f Makefile.local help       # Show all targets
  make -f Makefile.local test       # Run tests
  make -f Makefile.local lint       # Check code
  make -f Makefile.local format     # Format code
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

## Integration Notes

This orchestrator invokes these skills in order:

1. `pysmith:generating-pyproject`
2. `pysmith:generating-settings`
3. `pysmith:generating-precommit`
4. `makesmith:generating-local`

Each skill handles its own user interactions (merge vs overwrite, section selection, etc.).

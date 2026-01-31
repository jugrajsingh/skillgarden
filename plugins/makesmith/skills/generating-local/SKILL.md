---
name: generating-local
description: Generate Makefile.local with local development targets for Python projects. Supports configurable venv location (centralized ~/.venvs/ or project-local .venv).
allowed-tools:
  - Read
  - Write
  - Glob
  - AskUserQuestion
  - Bash(pwd)
  - Bash(basename *)
---

# Generate Makefile.local

Generate Makefile.local with local development targets. This file stores project-specific configuration (venv location) and provides standardized commands.

## Philosophy

- **Makefile.local for development** - Committed to repo, dev commands
- **Makefile.deploy for devops** - Separate file for build/push/deploy
- **Configurable venv location** - User chooses centralized or project-local
- **uv-native commands** - All commands use `uv run` or `uv sync`
- **Self-documenting** - `make -f Makefile.local help` shows all targets

## Workflow

### 1. Detect Project Name

```bash
basename $(pwd)
```

Use for default venv name and project identification.

### 2. Ask Venv Location

Present via AskUserQuestion:

```text
Where should the virtual environment be created?

○ ~/.venvs/{project_name}/  (Centralized)
  - Clean project directory
  - Survives git clean
  - Shared across worktrees

○ .venv/  (Project-local)
  - IDE auto-detects
  - Standard convention
  - Isolated per checkout
```

### 3. Check Existing Makefile.local

```text
Glob: Makefile.local
```

If exists, ask via AskUserQuestion:

- "Merge targets" - Keep custom targets, update standard ones
- "Overwrite" - Replace entirely
- "Skip" - Don't modify

### 4. Generate Makefile.local

**For centralized venv (`~/.venvs/{project}/`):**

```makefile
# =============================================================================
# Makefile.local - Local Development Commands
# =============================================================================
# Usage: make -f Makefile.local <target>
# Help:  make -f Makefile.local help
# =============================================================================

# Project configuration
PROJECT_NAME := {project_name}
VENV := $(HOME)/.venvs/$(PROJECT_NAME)

# Tell uv to use our venv location
export UV_PROJECT_ENVIRONMENT := $(VENV)

# Python paths
PYTHON := $(VENV)/bin/python
UV := uv

.DEFAULT_GOAL := help

.PHONY: help setup-local create-venv install install-dev install-hooks \
        test test-cov lint format type-check clean

# =============================================================================
# Setup
# =============================================================================

help:  ## Show available targets
 @grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup-local: create-venv install-dev install-hooks  ## Full local setup
 @echo ""
 @echo "============================================================================="
 @echo "Local setup complete!"
 @echo "============================================================================="
 @echo "Venv location: $(VENV)"
 @echo ""
 @echo "Next steps:"
 @echo "  1. cp example.env.yaml local.env.yaml"
 @echo "  2. Edit local.env.yaml with your settings"
 @echo "  3. make -f Makefile.local test"
 @echo "============================================================================="

create-venv:  ## Create virtual environment
 @if [ ! -d "$(VENV)" ]; then \
  echo "Creating venv at $(VENV)..."; \
  $(UV) venv $(VENV); \
 else \
  echo "Venv exists at $(VENV)"; \
 fi

# =============================================================================
# Dependencies
# =============================================================================

install:  ## Install production dependencies
 $(UV) sync --no-dev

install-dev:  ## Install all dependencies (production + dev)
 $(UV) sync

install-hooks: install-dev  ## Install pre-commit hooks
 $(UV) run pre-commit install

# =============================================================================
# Testing
# =============================================================================

test:  ## Run tests
 $(UV) run pytest

test-cov:  ## Run tests with coverage
 $(UV) run pytest --cov --cov-report=term-missing

test-watch:  ## Run tests in watch mode
 $(UV) run pytest --watch

# =============================================================================
# Code Quality
# =============================================================================

lint:  ## Run linter
 $(UV) run ruff check .

lint-fix:  ## Run linter with auto-fix
 $(UV) run ruff check . --fix

format:  ## Format code
 $(UV) run ruff format .

format-check:  ## Check formatting without changes
 $(UV) run ruff format . --check

type-check:  ## Run type checker
 $(UV) run mypy .

quality: lint format-check type-check  ## Run all quality checks

# =============================================================================
# Utilities
# =============================================================================

clean:  ## Remove build artifacts and caches
 rm -rf __pycache__ */__pycache__ */*/__pycache__
 rm -rf .pytest_cache .ruff_cache .mypy_cache
 rm -rf .coverage htmlcov
 rm -rf dist build *.egg-info
 @echo "Cleaned."

clean-venv:  ## Remove virtual environment
 rm -rf $(VENV)
 @echo "Removed venv at $(VENV)"

reset: clean clean-venv  ## Full reset (remove venv and caches)
 @echo "Reset complete. Run 'make -f Makefile.local setup-local' to start fresh."
```

**For project-local venv (`.venv/`):**

Same as above but with:

```makefile
VENV := .venv
```

### 5. Report

```text
Created Makefile.local:

Configuration:
  - Project: {project_name}
  - Venv: {venv_location}

Targets:
  setup-local   - Full local setup (venv + deps + hooks)
  install       - Install production dependencies
  install-dev   - Install all dependencies
  test          - Run tests
  lint          - Run linter
  format        - Format code
  type-check    - Run type checker
  clean         - Remove caches

Usage:
  make -f Makefile.local setup-local   # First time setup
  make -f Makefile.local test          # Run tests
  make -f Makefile.local lint          # Check code
```

## Integration with Other Skills

Other skills should use Makefile.local commands:

```bash
# Instead of: uv sync
make -f Makefile.local install-dev

# Instead of: uv run pytest
make -f Makefile.local test

# Instead of: uv run ruff check .
make -f Makefile.local lint
```

This ensures consistent venv location regardless of where it's configured.

## Adding Custom Targets

Users can add custom targets to Makefile.local:

```makefile
# =============================================================================
# Project-Specific Targets
# =============================================================================

run:  ## Run the application
 $(UV) run python main.py

migrate:  ## Run database migrations
 $(UV) run alembic upgrade head

seed:  ## Seed database with test data
 $(UV) run python scripts/seed.py
```

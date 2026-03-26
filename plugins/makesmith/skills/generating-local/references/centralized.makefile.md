# Centralized Venv Template (~/.venvs/)

Use this template when user selects `~/.venvs/{project_name}/`.

Replace `{project_name}` with actual project name from `basename $(pwd)`.

```makefile
# =============================================================================
# Makefile.local - Local Development Commands
# =============================================================================
# Usage: make -f Makefile.local <target>
# Help:  make -f Makefile.local help
# =============================================================================

PROJECT_NAME := {project_name}
VENV := $(HOME)/.venvs/$(PROJECT_NAME)
export UV_PROJECT_ENVIRONMENT := $(VENV)
export PYTHONPATH := $(CURDIR)

.DEFAULT_GOAL := help

# =============================================================================
# Setup
# =============================================================================
.PHONY: help setup-local

help:  ## Show available targets
 @grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-18s\033[0m %s\n", $$1, $$2}'

setup-local: install-dev install-hooks  ## Full local setup
 @echo "\n✓ Setup complete. Venv: $(VENV)"
 @echo "Next: cp example.env.yaml local.env.yaml && make -f Makefile.local test"

# =============================================================================
# Dependencies
# =============================================================================
.PHONY: install install-dev install-hooks

install:  ## Install production dependencies
 uv sync --no-dev

install-dev:  ## Install all dependencies
 uv sync

install-hooks: install-dev  ## Install pre-commit hooks
 uv run pre-commit install --install-hooks

# =============================================================================
# Testing
# =============================================================================
.PHONY: test test-unit test-integration test-cov

test:  ## Run all tests
 uv run pytest

test-unit:  ## Run unit tests only
 uv run pytest tests/unit/

test-integration:  ## Run integration tests only
 uv run pytest tests/integration/

test-cov:  ## Run tests with coverage
 uv run pytest --cov --cov-report=term-missing

# =============================================================================
# Code Quality
# =============================================================================
.PHONY: lint lint-fix format format-check type-check quality fix

lint:  ## Run linter
 uv run ruff check .

lint-fix:  ## Run linter with auto-fix
 uv run ruff check . --fix

format:  ## Format code
 uv run ruff format .

format-check:  ## Check formatting without fixing
 uv run ruff format . --check

type-check:  ## Run type checker
 uv run mypy .

quality: format-check lint type-check  ## Run all quality checks

fix: lint-fix format  ## Auto-fix lint + format

# =============================================================================
# Pre-commit
# =============================================================================
.PHONY: pre-commit pre-commit-all pre-commit-clean pre-commit-update

pre-commit:  ## Run pre-commit on staged files
 uv run pre-commit run

pre-commit-all:  ## Run pre-commit on all files
 uv run pre-commit run --all-files

pre-commit-clean:  ## Clean pre-commit cache and reinstall hooks
 uv run pre-commit clean
 uv run pre-commit install --install-hooks

pre-commit-update:  ## Update pre-commit hook versions
 uv run pre-commit autoupdate

# =============================================================================
# Scripts (project-specific — add targets as scripts are created)
# =============================================================================
# Pattern: each script gets a Makefile target so agents and developers
# run it with the correct arguments and environment variables.
#
# Example:
#   analyze-job:  ## Analyze batch job (JOB_ID=abc123)
#    uv run python scripts/analyze_job.py $(JOB_ID)

# =============================================================================
# Utilities
# =============================================================================
.PHONY: clean clean-venv reset

clean:  ## Remove caches
 rm -rf __pycache__ */__pycache__ */*/__pycache__ .pytest_cache .ruff_cache .mypy_cache .coverage htmlcov dist build *.egg-info

clean-venv:  ## Remove venv
 rm -rf $(VENV)

reset: clean clean-venv  ## Full reset
 @echo "✓ Reset complete. Run 'make -f Makefile.local setup-local' to start fresh."
```

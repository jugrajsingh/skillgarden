# Project-Local Venv Template (.venv/)

Use this template when user selects `.venv/` (recommended).

```makefile
# =============================================================================
# Makefile.local - Local Development Commands
# =============================================================================
# Usage: make -f Makefile.local <target>
# Help:  make -f Makefile.local help
# =============================================================================

VENV := .venv
export PYTHONPATH := $(CURDIR)

.DEFAULT_GOAL := help

# =============================================================================
# Setup
# =============================================================================
.PHONY: help setup-local

help:  ## Show available targets
 @grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-18s\033[0m %s\n", $$1, $$2}'

setup-local: install-dev install-hooks  ## Full local setup (uv sync creates .venv)
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
.PHONY: test test-cov

test:  ## Run tests
 uv run pytest

test-cov:  ## Run tests with coverage
 uv run pytest --cov --cov-report=term-missing

# =============================================================================
# Code Quality
# =============================================================================
.PHONY: lint lint-fix format type-check quality fix

lint:  ## Run linter
 uv run ruff check .

lint-fix:  ## Run linter with auto-fix
 uv run ruff check . --fix

format:  ## Format code
 uv run ruff format .

type-check:  ## Run type checker
 uv run mypy .

quality:  ## Run all quality checks (format → lint → types)
 uv run ruff format . --check
 uv run ruff check .
 uv run mypy .

fix: lint-fix format  ## Auto-fix lint + format

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

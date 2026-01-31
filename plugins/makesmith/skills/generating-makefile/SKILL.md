---
name: generating-makefile
description: Generate root Makefile that delegates to Makefile.local and Makefile.deploy with self-documenting help.
allowed-tools:
  - Read
  - Write
  - Glob
  - AskUserQuestion
  - Bash(pwd)
  - Bash(basename *)
---

# Generate Root Makefile

Create a root Makefile that serves as the project entrypoint, delegating to Makefile.local (dev) and Makefile.deploy (ops).

## Philosophy

- **Root Makefile is the entrypoint** - `make help` shows everything
- **Delegates to specialized files** - Makefile.local, Makefile.deploy
- **Box-drawing help banner** - Visual project identity
- **Project-specific targets** - Quick-run commands for the app

## Workflow

### 1. Detect Project Info

```bash
basename $(pwd)
```

### 2. Check Existing Files

```text
Glob: Makefile, Makefile.local, Makefile.deploy
```

If Makefile exists, ask via AskUserQuestion:

- "Merge targets" - Keep custom targets, add missing
- "Overwrite" - Replace entirely
- "Skip" - Don't modify

### 3. Generate Root Makefile

```makefile
# =============================================================================
# Makefile - {PROJECT_NAME}
# =============================================================================

.DEFAULT_GOAL := help

.PHONY: help install test lint format clean run

# =============================================================================
# Help
# =============================================================================

help:  ## Show available targets
 @echo ""
 @echo "╔══════════════════════════════════════════════╗"
 @echo "║  {PROJECT_NAME}                              ║"
 @echo "╠══════════════════════════════════════════════╣"
 @echo "║  Development: make -f Makefile.local help    ║"
 @echo "║  Deployment:  make -f Makefile.deploy help   ║"
 @echo "╚══════════════════════════════════════════════╝"
 @echo ""
 @grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# =============================================================================
# Development (delegates to Makefile.local)
# =============================================================================

install:  ## Install all dependencies
 $(MAKE) -f Makefile.local install-dev

test:  ## Run tests
 $(MAKE) -f Makefile.local test

lint:  ## Run linter
 $(MAKE) -f Makefile.local lint

format:  ## Format code
 $(MAKE) -f Makefile.local format

clean:  ## Remove build artifacts
 $(MAKE) -f Makefile.local clean

# =============================================================================
# Quick Run (project-specific)
# =============================================================================

run:  ## Run the application
 $(MAKE) -f Makefile.local run

# =============================================================================
# Deployment (delegates to Makefile.deploy)
# =============================================================================

build:  ## Build Docker image
 $(MAKE) -f Makefile.deploy build-image

push:  ## Push image to registry
 $(MAKE) -f Makefile.deploy push-image

deploy:  ## Deploy to Kubernetes
 $(MAKE) -f Makefile.deploy deploy

ship: build push deploy  ## Full CI/CD: build, push, deploy
```

### 4. Report

```text
Created root Makefile:

Delegates to:
  Makefile.local  - Development targets
  Makefile.deploy - Deployment targets

Quick targets:
  make install    -> make -f Makefile.local install-dev
  make test       -> make -f Makefile.local test
  make lint       -> make -f Makefile.local lint
  make build      -> make -f Makefile.deploy build-image
  make deploy     -> make -f Makefile.deploy deploy
  make ship       -> build + push + deploy

Usage:
  make help       # Show all targets
  make            # Same as make help
```

## Customization

Users should add project-specific targets to the "Quick Run" section:

```makefile
run-api:  ## Run API server
 $(MAKE) -f Makefile.local run-api

run-worker:  ## Run background worker
 $(MAKE) -f Makefile.local run-worker
```

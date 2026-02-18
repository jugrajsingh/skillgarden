---
name: generating-makefile
description: Use when a project needs a root Makefile that delegates to Makefile.local and Makefile.deploy with a self-documenting help banner
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

Read `references/root-makefile-template.makefile` and customize:

- Replace `{PROJECT_NAME}` with detected project name
- Adjust box-drawing banner width to fit project name
- If no Makefile.deploy exists, remove Deployment section targets
- If no Makefile.local exists, remove Development section targets

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

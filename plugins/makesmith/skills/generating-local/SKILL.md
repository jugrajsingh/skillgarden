---
name: generating-local
description: Generate Makefile.local with local development targets for Python projects. Supports configurable venv location (project-local .venv recommended, or centralized ~/.venvs/).
allowed-tools:
  - Read
  - Write
  - Glob
  - AskUserQuestion
  - Bash(pwd)
  - Bash(basename *)
---

# Generate Makefile.local

Generate Makefile.local with local development targets. This file stores project-specific configuration (venv location, PYTHONPATH) and provides standardized commands.

## Philosophy

- **Makefile.local for development** - Committed to repo, dev commands
- **Makefile.deploy for devops** - Separate file for build/push/deploy
- **Project-local `.venv/` recommended** - Standard convention, IDE-friendly
- **PYTHONPATH always exported** - Enables bare imports without build system
- **uv-native commands** - All commands use `uv run` or `uv sync`
- **Self-documenting** - `make -f Makefile.local help` shows all targets

## Templates

Templates are in `references/` folder:

- `references/project-local.makefile.md` - For `.venv/` (recommended)
- `references/centralized.makefile.md` - For `~/.venvs/{project}/`

## Workflow

### 1. Detect Project Name

```bash
basename $(pwd)
```

Use for default venv name and project identification.

### 2. Ask Venv Location

Present via AskUserQuestion with `.venv/` as recommended (first option):

```yaml
question: "Where should the virtual environment be created?"
header: "Venv location"
options:
  - label: ".venv/ (Recommended)"
    description: "IDE auto-detects, standard uv convention, isolated per checkout"
  - label: "~/.venvs/{project_name}/"
    description: "Clean project directory, survives git clean, shared across worktrees"
```

### 3. Check Existing Makefile.local

```text
Glob: Makefile.local
```

If exists, ask via AskUserQuestion:

- "Overwrite" - Replace entirely with new template
- "Skip" - Don't modify

### 4. Read Template

Based on user's venv choice:

**For `.venv/` (recommended):**

```text
Read: references/project-local.makefile.md
```

**For `~/.venvs/`:**

```text
Read: references/centralized.makefile.md
```

Extract the makefile content from the markdown code block.

### 5. Generate Makefile.local

**For project-local (`.venv/`):**

- Write template as-is (no placeholders to replace)

**For centralized (`~/.venvs/`):**

- Replace `{project_name}` with actual project name

Write to `Makefile.local`.

### 6. Report

```text
Created Makefile.local:

Configuration:
  - Venv: {venv_location}
  - PYTHONPATH: exported (enables bare imports)

Targets:
  setup-local   - Full local setup (deps + hooks)
  install-dev   - Install all dependencies
  test          - Run tests
  lint          - Run linter
  format        - Format code
  type-check    - Run type checker
  quality       - Run all quality checks
  fix           - Auto-fix lint + format
  clean         - Remove caches
  reset         - Full reset

Usage:
  make -f Makefile.local setup-local   # First time setup
  make -f Makefile.local test          # Run tests
  make -f Makefile.local quality       # Check code
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

This ensures consistent venv location and PYTHONPATH regardless of configuration.

## Adding Custom Targets

Users can add project-specific targets:

```makefile
# =============================================================================
# Application
# =============================================================================
.PHONY: run run-dev

run:  ## Run the application
 uv run python main.py

run-dev:  ## Run with auto-reload
 uv run python main.py --reload

# =============================================================================
# Infrastructure
# =============================================================================
.PHONY: infra-up infra-down

infra-up:  ## Start Docker services
 docker compose up -d --wait

infra-down:  ## Stop Docker services
 docker compose down
```

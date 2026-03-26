---
name: generating-local
description: Use when a Python project needs a Makefile.local for local development targets (test, lint, format, setup) with configurable venv location
allowed-tools:
  - Read
  - Write
  - Glob
  - Bash(pwd)
  - Bash(basename *)
  - AskUserQuestion
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
- **Agent-first** - CLAUDE.md updated so agents always use Makefile targets

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

### 6. Update CLAUDE.md Commands Section

After generating Makefile.local, update the project's CLAUDE.md to instruct agents to use Makefile targets. This is critical — without it, agents bypass the Makefile and run raw commands.

**Read the generated Makefile.local** and extract all targets with `## descriptions`.

**Find or create the `## Commands` section in CLAUDE.md.** If CLAUDE.md doesn't exist, create a minimal one. If the Commands section exists, replace it entirely.

**Generate the Commands section:**

````markdown
## Commands

**CRITICAL: Never run commands directly. Always use Makefile.local.**

```bash
make -f Makefile.local setup-local    # Full local setup
make -f Makefile.local install-dev    # Install dependencies
make -f Makefile.local test           # Run all tests
make -f Makefile.local test-unit      # Unit tests only
make -f Makefile.local lint           # Run linter
make -f Makefile.local type-check     # Type checking
make -f Makefile.local quality        # All quality checks (lint + format + type-check)
make -f Makefile.local pre-commit     # Run pre-commit hooks
make -f Makefile.local clean          # Remove caches
```

**NEVER run directly:** `pip install`, `uv sync`, `uv run`, `python`, `pytest`, `ruff`, `mypy`
````

Include all targets from the actual generated Makefile, including any project-specific Script targets. If Makefile.deploy exists, also include its key targets (build-image, push-image, deploy) in a separate block.

**Why this matters:** Agents rely on CLAUDE.md as their primary instruction set. Without explicit Makefile commands, they default to raw `uv run pytest`, `python main.py`, etc., which fails when projects need specific env vars, credential paths, or submodule excludes.

### 7. Report

```text
Created Makefile.local:

Configuration:
  - Venv: {venv_location}
  - PYTHONPATH: exported (enables bare imports)

Targets:
  setup-local     - Full local setup (deps + hooks)
  install-dev     - Install all dependencies
  test            - Run all tests
  test-unit       - Run unit tests only
  test-integration - Run integration tests
  lint            - Run linter
  format          - Format code
  format-check    - Check formatting
  type-check      - Run type checker
  quality         - All quality checks
  fix             - Auto-fix lint + format
  pre-commit      - Run pre-commit hooks
  clean           - Remove caches
  reset           - Full reset

Updated CLAUDE.md:
  - Commands section updated with all Makefile targets

Usage:
  make -f Makefile.local setup-local   # First time setup
  make -f Makefile.local test          # Run tests
  make -f Makefile.local quality       # Check code
```

## Integration

Other skills should use Makefile.local commands instead of raw uv commands (`make -f Makefile.local test` instead of `uv run pytest`). This ensures consistent venv location and PYTHONPATH.

## Custom Targets

Users can add project-specific targets to these sections:

- **Application** — `run`, `run-dev`, `run-{source}` for multi-deployment apps
- **Infrastructure** — `infra-up`, `infra-down`, `bootstrap` for Docker/DB setup
- **Scripts** — One target per script, with correct env vars and arguments

All custom targets should follow the `.PHONY` + `## description` pattern for self-documentation and help output.

When adding script targets, the agent MUST also update the CLAUDE.md Commands section to include the new target.

## Scripts Section Convention

The template includes a Scripts section with a comment-only placeholder. When agents create scripts for a project, they should:

1. Add a Makefile target with the correct env vars and arguments
2. Update CLAUDE.md Commands section to include the new target
3. Use the `## description` pattern so `make help` shows it

This ensures all scripts are discoverable and runnable with the correct configuration, rather than requiring developers to guess credential paths or argument formats.

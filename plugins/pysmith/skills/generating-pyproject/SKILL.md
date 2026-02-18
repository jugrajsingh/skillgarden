---
name: generating-pyproject
description: Generate pyproject.toml with uv-native dependency management and tool configurations (ruff, pytest, mypy, coverage). Use when starting a new Python project, migrating from requirements.txt to uv, or setting up modern Python tooling.
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
  - Bash(uv *)
---

# Generate pyproject.toml (uv-native)

Create or update pyproject.toml with dependencies and tool configurations.

## Philosophy

- **pyproject.toml is the single source of truth** - Dependencies AND tool configs
- **uv for package management** - `uv add`, `uv sync`, `uv run`
- **No requirements.txt** - Migrate existing deps to pyproject.toml
- Use ruff (replaces black, isort, flake8, pylint)
- Google-style docstrings, 120 character line length

## Workflow

### 1. Check Existing Files

```text
Glob: pyproject.toml, requirements*.txt
```

**If pyproject.toml exists**, ask via AskUserQuestion:

- "Merge with existing" - Keep custom settings, add missing sections
- "Overwrite" - Replace entirely
- "Skip" - Don't modify

**If requirements.txt exists**, ask via AskUserQuestion:

- "Migrate to pyproject.toml" - Parse deps and add to [project.dependencies]
- "Keep both" - Generate pyproject.toml, leave requirements.txt
- "Skip migration" - Ignore requirements.txt

### 2. Detect Project Info

Check for project name in:

- Existing pyproject.toml `[project].name`
- Directory name (fallback)

### 3. Generate pyproject.toml

Read the template from `references/pyproject-template.toml` and customize:

- Set `name` to detected project name
- Adjust `requires-python` if needed
- Add project-specific dependencies to `[project].dependencies`
- Add project-specific dev deps to `[dependency-groups].dev`

### 4. Migration from requirements.txt

When migrating, parse requirements.txt and categorize:

**Production deps** -> `[project].dependencies`:

```text
pydantic>=2.0
httpx>=0.27.0
aiobotocore>=2.15.0
```

**Dev deps** (pytest, ruff, mypy, pre-commit, etc.) -> `[dependency-groups].dev`:

```text
pytest>=8.0
ruff>=0.8
mypy>=1.11
```

After migration, ask:

- "Delete requirements.txt" - Remove migrated file
- "Keep as backup" - Rename to requirements.txt.bak
- "Keep unchanged" - Leave file in place

### 5. Initialize uv Lock

After generating pyproject.toml:

```bash
uv sync
```

This creates `uv.lock` with resolved dependencies.

### 6. Report

```text
Created pyproject.toml (uv-native) with:

[project]
  - name: {project_name}
  - dependencies: {n} production packages

[dependency-groups]
  - dev: {n} development packages

[tool.*]
  - ruff: linting + formatting (120 char, google docstrings)
  - pytest: async mode, strict markers
  - mypy: type checking
  - coverage: source tracking

Commands:
  uv add <package>        # Add production dependency
  uv add --dev <package>  # Add dev dependency
  uv sync                 # Install all dependencies
  uv run pytest           # Run tests
  uv run ruff check .     # Lint code
  uv run ruff format .    # Format code
```

## Dependency Management with uv

| Task | Command |
|------|---------|
| Add production dep | `uv add package` |
| Add dev dep | `uv add --dev package` |
| Remove dep | `uv remove package` |
| Sync deps | `uv sync` |
| Run tool | `uv run tool` |
| Update lockfile | `uv lock --upgrade` |

## Ruff Rule Categories

| Code | Category |
|------|----------|
| F | Pyflakes |
| E, W | pycodestyle |
| I | isort |
| N | pep8-naming |
| D | pydocstyle |
| UP | pyupgrade |
| S | bandit (security) |
| B | flake8-bugbear |
| C4 | flake8-comprehensions |
| PT | flake8-pytest-style |
| RUF | ruff-specific |

## Common Dependency Groups

**Web frameworks:**

```toml
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.32.0",
]
```

**Async/AWS:**

```toml
dependencies = [
    "aiobotocore>=2.15.0",
    "httpx>=0.27.0",
]
```

**Database:**

```toml
dependencies = [
    "sqlalchemy>=2.0",
    "asyncpg>=0.29.0",
    "alembic>=1.13.0",
]
```

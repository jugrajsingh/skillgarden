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

```toml
[project]
name = "{project_name}"
version = "0.1.0"
description = ""
requires-python = ">=3.11"
dependencies = [
    "pydantic>=2.0",
    "pydantic-settings[yaml]>=2.0",
]

[dependency-groups]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.24",
    "pytest-cov>=5.0",
    "mypy>=1.11",
    "ruff>=0.8",
    "pre-commit>=4.0",
]

# =============================================================================
# Tool Configurations
# =============================================================================

[tool.ruff]
line-length = 120
target-version = "py311"
exclude = [
    ".git",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    ".eggs",
    ".idea",
    ".pytest_cache",
    ".mypy_cache",
]

[tool.ruff.lint]
select = [
    "F", "E", "W", "C90", "I", "N", "D", "UP", "YTT", "ANN", "ASYNC",
    "S", "BLE", "FBT", "B", "A", "COM", "C4", "DTZ", "T10", "EM",
    "EXE", "FA", "ISC", "ICN", "G", "INP", "PIE", "T20", "PYI", "PT",
    "Q", "RSE", "RET", "SLF", "SLOT", "SIM", "TID", "TCH", "INT",
    "ARG", "PTH", "TD", "FIX", "ERA", "PD", "PGH", "PL", "TRY",
    "FLY", "NPY", "AIR", "PERF", "FURB", "LOG", "RUF",
]

ignore = [
    "D100", "D101", "D102", "D103", "D104", "D105", "D107",  # Missing docstrings
    "ANN401",  # Dynamically typed expressions
    "S101", "S311",  # Assert, pseudo-random
    "FBT001", "FBT002", "FBT003",  # Boolean args
    "B008",  # Function calls in defaults
    "COM812", "ISC001",  # Conflicts with formatter
    "UP007",  # Use X | Y (prefer Optional[X])
    "EM101", "EM102", "TRY003",  # Exception messages
    "RET504",  # Unnecessary assignment
    "PLR0913", "PLR2004",  # Too many args, magic values
    "TD002", "TD003", "FIX002",  # TODO comments
    "CPY001",  # Copyright notice
    "G004",  # Logging f-strings
]

[tool.ruff.lint.per-file-ignores]
"tests/*" = ["S101", "ANN", "D", "PLR2004"]
"scripts/*" = ["T20", "INP001"]

[tool.ruff.lint.pydocstyle]
convention = "google"

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

[tool.pytest.ini_options]
asyncio_mode = "auto"
asyncio_default_fixture_loop_scope = "function"
testpaths = ["tests"]
addopts = ["-v", "--strict-markers"]
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
]

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
ignore_missing_imports = true

[tool.coverage.run]
source = ["."]
omit = ["*/tests/*", "*/__pycache__/*", "*/site-packages/*", ".venv/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
]
```

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

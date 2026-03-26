# Python Makefile Audit Checks

Language-specific checks for Python projects using uv.

## Detection

Load this reference when any of these are found:

```text
Glob: pyproject.toml, requirements.txt, uv.lock, setup.py
```

## Makefile.local Checks

### Command Runner

| Check | Pass Criteria | Priority |
|-------|---------------|----------|
| uv run usage | All python/pytest/ruff/mypy commands use `uv run`, no bare `python` | High |
| No pip commands | No `pip install`, `pip freeze`, `pip list` in recipes | High |
| No bare python | `PYTHON := python` is wrong, should use `uv run python` or call `uv run` directly | High |

### Required Variables

| Check | Pass Criteria | Priority |
|-------|---------------|----------|
| VENV defined | `VENV := .venv` present | Medium |
| PYTHONPATH exported | `export PYTHONPATH := $(CURDIR)` present | Medium |

### Required Targets

| Target | Expected Command | Priority |
|--------|-----------------|----------|
| `install` or `install-dev` | `uv sync` | High |
| `test` | `uv run pytest` | High |
| `test-unit` | `uv run pytest tests/unit/` | High |
| `lint` | `uv run ruff check .` | High |
| `format` | `uv run ruff format .` | Medium |
| `format-check` | `uv run ruff format . --check` | Medium |
| `type-check` | `uv run mypy .` | Medium |
| `quality` | Prerequisite target: `format-check lint type-check` | Medium |
| `fix` | `lint-fix` + `format` combined | Low |
| `clean` | Remove `__pycache__`, `.pytest_cache`, `.ruff_cache`, `.mypy_cache` | Medium |
| `setup-local` | `install-dev` + `install-hooks` | Medium |
| `pre-commit` | `uv run pre-commit run` | Medium |
| `pre-commit-all` | `uv run pre-commit run --all-files` | Low |

### Quality Target Convention

The `quality` target MUST use prerequisite targets, not inline commands:

```makefile
# CORRECT — uses prerequisite targets, each can run independently
quality: format-check lint type-check  ## Run all quality checks

# WRONG — inline commands, format-check not reusable as standalone target
quality:  ## Run all quality checks
 uv run ruff format . --check
 uv run ruff check .
 uv run mypy .
```

### CLAUDE.md Integration

| Check | Pass Criteria | Priority |
|-------|---------------|----------|
| Commands section exists | CLAUDE.md has a `## Commands` section listing Makefile targets | High |
| NEVER instruction present | Contains `**NEVER run directly:**` with list of banned commands | High |
| Targets match Makefile | Listed commands match actual Makefile.local targets | Medium |
| Script targets included | Project-specific script targets from Makefile.local are documented | Medium |

### Anti-Patterns

| Pattern | Issue | Fix |
|---------|-------|-----|
| `$(PYTHON) main.py` with `PYTHON := python` | Bypasses uv venv | Use `uv run python main.py` |
| `pytest` without `uv run` | Uses system pytest | Use `uv run pytest` |
| `pip install -r requirements.txt` | Legacy package management | Use `uv sync` |
| `virtualenv .venv` or `python -m venv` | Manual venv creation | `uv sync` creates venv automatically |
| `source .venv/bin/activate` in recipes | Activation not needed with `uv run` | Use `uv run` prefix |
| `UV := uv` variable | Unnecessary indirection | Use `uv` directly in recipes |
| Inline commands in `quality` target | `format-check` not standalone | Use prerequisite targets |
| Missing CLAUDE.md Commands section | Agents bypass Makefile | Add Commands section with all targets |

## Makefile.deploy Checks

### Python-Specific Deploy Patterns

| Check | Pass Criteria | Priority |
|-------|---------------|----------|
| No dev deps in image | `uv sync --no-dev` or `--no-dev` flag used in Dockerfile reference | Low |
| No .venv in build context | `.dockerignore` should exclude `.venv/` | Medium |
| VERSION line clean | No trailing characters in `VERSION := $(shell git describe ...)` | High |

## pyproject.toml Consistency

The Makefile targets assume specific tool configurations in `pyproject.toml`. Audit for alignment:

| Makefile Target | pyproject.toml Requirement | Priority |
|--------|---------|----------|
| `lint` (`ruff check .`) | `[tool.ruff]` section with `line-length`, `target-version`, rules | High |
| `format` (`ruff format .`) | `[tool.ruff.format]` with `quote-style = "double"` | Medium |
| `type-check` (`mypy .`) | `[tool.mypy]` section with `python_version`, `ignore_missing_imports` | Medium |
| `test` (`pytest`) | `[tool.pytest.ini_options]` with `testpaths`, `asyncio_mode` | Medium |
| `test-cov` (`pytest --cov`) | `[tool.coverage]` with `source`, `omit` | Low |

If any `[tool.*]` section is missing, the corresponding Makefile target will use defaults which may cause inconsistent behavior across repos.

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
| `lint` | `uv run ruff check .` | High |
| `format` | `uv run ruff format .` | Medium |
| `type-check` | `uv run mypy .` | Medium |
| `quality` | Combined format-check + lint + types | Medium |
| `fix` | `lint-fix` + `format` combined | Low |
| `clean` | Remove `__pycache__`, `.pytest_cache`, `.ruff_cache`, `.mypy_cache` | Medium |
| `setup-local` | `install-dev` + `install-hooks` | Low |

### Anti-Patterns

| Pattern | Issue | Fix |
|---------|-------|-----|
| `$(PYTHON) main.py` with `PYTHON := python` | Bypasses uv venv | Use `uv run python main.py` |
| `pytest` without `uv run` | Uses system pytest | Use `uv run pytest` |
| `pip install -r requirements.txt` | Legacy package management | Use `uv sync` |
| `virtualenv .venv` or `python -m venv` | Manual venv creation | `uv sync` creates venv automatically |
| `source .venv/bin/activate` in recipes | Activation not needed with `uv run` | Use `uv run` prefix |

## Makefile.deploy Checks

### Python-Specific Deploy Patterns

| Check | Pass Criteria | Priority |
|-------|---------------|----------|
| No dev deps in image | `uv sync --no-dev` or `--no-dev` flag used in Dockerfile reference | Low |
| No .venv in build context | `.dockerignore` should exclude `.venv/` | Medium |

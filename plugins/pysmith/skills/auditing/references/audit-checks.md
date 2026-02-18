# Audit Checks

## Configuration (pyproject.toml)

| Check | Pass Criteria |
|-------|---------------|
| pyproject.toml exists | File present at project root |
| ruff configured | [tool.ruff] section with line-length and select rules |
| Rule coverage | At minimum: F, E, W, I, N, S, B, C4, UP, RUF selected |
| pytest configured | [tool.pytest.ini_options] with testpaths |
| mypy configured | [tool.mypy] section present |
| coverage configured | [tool.coverage.run] with source and omit |
| Dev deps present | [dependency-groups] dev includes pytest, ruff, mypy, pre-commit |
| Google docstrings | [tool.ruff.lint.pydocstyle] convention = "google" |

## Settings Management

| Check | Pass Criteria |
|-------|---------------|
| No os.getenv() in app code | Grep for os.getenv outside tests/ and scripts/ |
| No hardcoded secrets | Grep for password=, secret=, api_key= with literal string values |
| Pydantic Settings used | config/settings.py or settings.py with BaseSettings |
| YAML support configured | yaml_file in SettingsConfigDict |
| example.env.yaml exists | Template committed for local dev |
| gitignore updated | *.env.yaml ignored, example.env.yaml excluded from ignore |

## Pre-commit Hooks

| Check | Pass Criteria |
|-------|---------------|
| .pre-commit-config.yaml exists | File present |
| gitleaks hook present | Secrets detection enabled |
| pip-audit hook present | Dependency vulnerability scanning |
| ruff hooks present | Both ruff-format and ruff (format before lint) |
| No redundant tools | No black, isort, flake8, bandit alongside ruff |
| Hook ordering | Security → Autofix → Lint+fix → Validation → Git quality |
| Branch protection | no-commit-to-branch for main/develop |

## Project Structure

| Check | Pass Criteria |
|-------|---------------|
| tests/ directory exists | Test directory present |
| conftest.py exists | Shared fixtures file in tests/ |
| __init__.py files present | Package directories have __init__.py |
| src/ or flat layout consistent | Not mixing both patterns |

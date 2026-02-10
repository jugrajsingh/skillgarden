---
name: auditing
description: Audit Python project against best practices for pyproject.toml, settings management, pre-commit hooks, and project structure.
allowed-tools:
  - Read
  - Glob
  - Grep
  - AskUserQuestion
---

# Audit Python Project

Analyze a Python project against best practices and generate a structured report.

## Checks

### Configuration (pyproject.toml)

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

### Settings Management

| Check | Pass Criteria |
|-------|---------------|
| No os.getenv() in app code | Grep for os.getenv outside tests/ and scripts/ |
| No hardcoded secrets | Grep for password=, secret=, api_key= with literal string values |
| Pydantic Settings used | config/settings.py or settings.py with BaseSettings |
| YAML support configured | yaml_file in SettingsConfigDict |
| example.env.yaml exists | Template committed for local dev |
| gitignore updated | *.env.yaml ignored, example.env.yaml excluded from ignore |

### Pre-commit Hooks

| Check | Pass Criteria |
|-------|---------------|
| .pre-commit-config.yaml exists | File present |
| gitleaks hook present | Secrets detection enabled |
| pip-audit hook present | Dependency vulnerability scanning |
| ruff hooks present | Both ruff-format and ruff (format before lint) |
| No redundant tools | No black, isort, flake8, bandit alongside ruff |
| Hook ordering | Security → Autofix → Lint+fix → Validation → Git quality |
| Branch protection | no-commit-to-branch for main/develop |

### Project Structure

| Check | Pass Criteria |
|-------|---------------|
| tests/ directory exists | Test directory present |
| conftest.py exists | Shared fixtures file in tests/ |
| __init__.py files present | Package directories have __init__.py |
| src/ or flat layout consistent | Not mixing both patterns |

## Workflow

### 1. Scan Project

```text
Glob: pyproject.toml, config/settings.py, **/settings.py, .pre-commit-config.yaml,
      tests/, tests/conftest.py, **/__init__.py, src/
```

### 2. Run Checks

For each category, evaluate pass/fail and collect details.

### 3. Search for Anti-patterns

```text
Grep: os.getenv, os.environ.get (in *.py excluding tests/)
Grep: password\s*=\s*["'], secret\s*=\s*["'], api_key\s*=\s*["'] (in *.py)
```

### 4. Generate Report

Use the audit-report.md template. Fill in:

- Each check with ✓ (pass), ✗ (fail), or △ (partial/uncertain)
- Findings grouped by category
- Recommendations sorted by priority (high/medium/low)

### 5. Ask About Fixes

After presenting the report, ask via AskUserQuestion:

- "Fix all issues" - Invoke relevant pysmith skills to fix
- "Fix critical only" - Only fix high-priority items
- "Report only" - No changes, just the audit report

## Report Output

Write to `docs/audits/python-audit-{date}.md` or display inline if docs/ doesn't exist.

## Priority Classification

| Priority | Criteria |
|----------|----------|
| High | Security issues, missing secrets detection, hardcoded credentials |
| Medium | Missing tool configs, incomplete rule coverage, no branch protection |
| Low | Structure improvements, missing conftest.py, documentation gaps |

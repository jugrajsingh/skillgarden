---
name: auditing
description: Use when checking a Python project for configuration gaps, missing tool configs, hardcoded secrets, or pre-commit hook issues
allowed-tools:
  - Read
  - Glob
  - Grep
  - AskUserQuestion
---

# Audit Python Project

Analyze a Python project against best practices and generate a structured report.

## Checks

Read `references/audit-checks.md` for the full checklist. Five categories:

1. **Configuration** (pyproject.toml) - ruff, pytest, mypy, coverage, dev deps, docstyle
2. **Settings Management** - no os.getenv(), no hardcoded secrets, Pydantic Settings, YAML
3. **Pre-commit Hooks** - gitleaks, pip-audit, ruff, no redundant tools, ordering, branch protection
4. **Project Structure** - tests/, conftest.py, **init**.py, consistent layout
5. **Makefile Integration** - Makefile.local exists, CLAUDE.md Commands section, tool alignment

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

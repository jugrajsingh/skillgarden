---
name: generating-precommit
description: Generate .pre-commit-config.yaml with security scanning, linting, and formatting hooks
allowed-tools:
  - Read
  - Write
  - Glob
  - AskUserQuestion
---

# Generate Pre-commit Config

Create optimized .pre-commit-config.yaml for Python projects.

## Tool Selection Rationale

**Ruff replaces:** black, autopep8, autoflake, isort, flake8, flake8-bandit

**Still needed:**

- **gitleaks** - Secrets detection (not Python-specific)
- **pip-audit** - Dependency vulnerabilities (not covered by ruff)
- **pre-commit-hooks** - File validation, merge conflicts

**Dropped:**

- bandit → ruff S rules cover security checks
- black → ruff format is identical, faster
- isort → ruff I rules
- flake8 → ruff check

## Workflow

### 1. Check Existing Config

```text
Glob: .pre-commit-config.yaml
```

If exists, ask via AskUserQuestion:

- "Merge hooks" - Keep custom hooks, update versions
- "Overwrite" - Replace entirely
- "Skip" - Don't modify

### 1b. Detect Redundant Tools

If existing config contains black, isort, flake8, autopep8, autoflake, or bandit, ask:

```text
question: "Detected tools that ruff replaces. Migrate to ruff?"
header: "Migration"
options:
  - label: "Yes, replace with ruff"
    description: "Remove black/isort/flake8/bandit, use ruff instead"
  - label: "No, keep existing"
    description: "Keep current setup unchanged"
```

Tools ruff replaces:

- black → ruff format
- isort → ruff I rules
- flake8 → ruff check
- bandit → ruff S rules
- autopep8 → ruff format
- autoflake → ruff check

### 2. Generate .pre-commit-config.yaml

Read the base config from `references/pre-commit-base.yaml` and use it as the starting template.

**Customizations to apply based on project context:**

- If no `chart/` directory, remove the `exclude: '^chart/templates/'` from check-yaml
- If project uses markdown files, uncomment the markdownlint section
- If project uses Makefiles, uncomment the mbake section
- If project uses Docker, uncomment the hadolint section
- If project has strict typing, uncomment the mypy section

Copy the base config to `.pre-commit-config.yaml` with applicable sections uncommented.

### 4. Report

```text
Created .pre-commit-config.yaml

Hook ordering (autofix first to minimize retries):
  1. Security:    gitleaks, pip-audit, detect-private-key
  2. Autofix:     whitespace fixers (end-of-file, trailing, line-ending)
  3. Ruff:        ruff-format THEN ruff --fix (format before lint)
  4. Validation:  check-ast, check-yaml/json/toml, debug-statements
  5. Git quality: no-commit-to-branch, check-merge-conflict
  6. Commits:     conventional-pre-commit (commit-msg stage)

Ruff replaces: black, isort, flake8, bandit, autopep8

Install: pre-commit install
Run all: pre-commit run --all-files
Update:  pre-commit autoupdate
```

## Why No Bandit?

Ruff's `S` rules (flake8-bandit) cover the same security checks:

- S101: assert_used
- S102: exec_used
- S103: bad_file_permissions
- S104: hardcoded_bind_all_interfaces
- S105-S108: hardcoded passwords/secrets
- S301-S303: pickle, marshal, insecure hash
- S311: pseudo-random generators
- S501-S509: SSL/TLS issues
- S601-S612: shell injection, SQL injection

Enable in pyproject.toml:

```toml
[tool.ruff.lint]
select = ["S"]  # Security rules
```

## Version Updates

Check latest versions:

- <https://github.com/gitleaks/gitleaks/releases>
- <https://github.com/astral-sh/ruff-pre-commit/releases>
- <https://github.com/pre-commit/pre-commit-hooks/releases>
- <https://github.com/pypa/pip-audit/releases>

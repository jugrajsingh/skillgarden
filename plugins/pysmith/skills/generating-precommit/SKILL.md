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

```yaml
# Pre-commit hooks configuration
# Install: pre-commit install
# Run all: pre-commit run --all-files
# Update:  pre-commit autoupdate

minimum_pre_commit_version: 3.6.0
fail_fast: true
exclude: '^(\.git|\.venv|build|dist|node_modules|\.idea)'

repos:
  # ============================================================
  # SECURITY (External tools - not covered by ruff)
  # ============================================================

  # Detect secrets, API keys, credentials in any file type
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.21.2
    hooks:
      - id: gitleaks

  # Scan dependencies for known vulnerabilities
  - repo: https://github.com/pypa/pip-audit
    rev: v2.7.3
    hooks:
      - id: pip-audit
        args: ["--desc", "--format=columns"]

  # ============================================================
  # STANDARD CHECKS
  # ============================================================

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      # Security
      - id: detect-private-key
      - id: check-added-large-files
        args: ["--maxkb=1000"]

      # Branch protection
      - id: no-commit-to-branch
        args:
          - --branch=main
          - --branch=develop

      # Python validation
      - id: check-ast
      - id: debug-statements

      # File format validation
      - id: check-yaml
        exclude: '^chart/templates/'
      - id: check-json
      - id: check-toml

      # Git hygiene
      - id: check-merge-conflict
      - id: check-case-conflict

      # Whitespace (auto-fix)
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: mixed-line-ending
        args: ["--fix=lf"]

  # ============================================================
  # PYTHON: RUFF (replaces black, isort, flake8, bandit, autopep8)
  # ============================================================

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.6
    hooks:
      # Linting with auto-fix (includes security S rules)
      - id: ruff
        args: ["--fix"]
      # Formatting (replaces black)
      - id: ruff-format
```

### 3. Optional Additions

**Typo detection (recommended for docs-heavy projects):**

```yaml
  - repo: https://github.com/codespell-project/codespell
    rev: v2.3.0
    hooks:
      - id: codespell
        args: ["--skip", "*.lock,*.svg"]
```

**Markdown linting (if .md files present):**

```yaml
  - repo: https://github.com/igorshubovych/markdownlint-cli
    rev: v0.42.0
    hooks:
      - id: markdownlint
        args: ["--fix"]
```

**Type checking (for strict type safety):**

```yaml
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.13.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

### 4. Report

```text
Created .pre-commit-config.yaml

Hooks installed:
  Security:     gitleaks, pip-audit, detect-private-key
  Validation:   check-ast, check-yaml/json/toml, debug-statements
  Git hygiene:  no-commit-to-branch, check-merge-conflict
  Formatting:   ruff (lint+fix), ruff-format, whitespace fixes

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

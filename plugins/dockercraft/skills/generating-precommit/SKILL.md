---
name: generating-precommit
description: Generate pre-commit hooks for Dockerfile linting with hadolint
allowed-tools:
  - Read
  - Write
  - Glob
  - AskUserQuestion
---

# Docker Pre-commit Hooks

Add Dockerfile linting to pre-commit configuration.

## Tool: Hadolint

Hadolint is the standard Dockerfile linter. It:

- Validates Dockerfile syntax
- Checks for best practices (DL codes)
- Validates shell commands with ShellCheck (SC codes)

## Workflow

### 1. Check for Dockerfiles

```text
Glob: **/Dockerfile, **/Dockerfile.*, **/*.dockerfile
```

If no Dockerfiles found, report and exit.

### 2. Check Existing Pre-commit Config

```text
Glob: .pre-commit-config.yaml
```

If exists, merge hadolint hook. If not, create minimal config.

### 3. Add Hadolint Hook

```yaml
  # Dockerfile linting
  - repo: https://github.com/hadolint/hadolint
    rev: v2.12.0
    hooks:
      - id: hadolint-docker
        args: ["--ignore", "DL3008", "--ignore", "DL3013"]
```

### 4. Common Ignores

| Code | Rule | When to Ignore |
|------|------|----------------|
| DL3008 | Pin apt versions | Dev images where latest is OK |
| DL3013 | Pin pip versions | When using requirements.txt |
| DL3018 | Pin apk versions | Alpine dev images |
| DL3059 | Multiple consecutive RUN | Readability preference |

### 5. Optional: .hadolint.yaml Config

Create project-level config for consistent ignores:

```yaml
# .hadolint.yaml
ignored:
  - DL3008  # apt-get version pinning
  - DL3013  # pip version pinning

trustedRegistries:
  - docker.io
  - gcr.io
  - ghcr.io
```

### 6. Report

```text
Added Docker linting to pre-commit:

Hook: hadolint-docker
Files: Dockerfile, Dockerfile.*, *.dockerfile

Common commands:
  hadolint Dockerfile           # Lint single file
  hadolint --ignore DL3008 ...  # Ignore specific rule

Docs: https://github.com/hadolint/hadolint
```

## Best Practice Rules

**Security (critical):**

- DL3002: Last USER should not be root
- DL3004: Do not use sudo
- DL4006: Set SHELL with pipefail

**Efficiency:**

- DL3003: Use WORKDIR instead of cd
- DL3020: Use COPY instead of ADD for files
- DL3025: Use JSON for CMD arguments

**Maintainability:**

- DL3006: Always tag base image version
- DL3007: Avoid using latest tag

---
name: init
description: Initialize git-flow configuration for a repository
allowed-tools:
  - Bash(git *)
  - Bash(which *)
---

# Git Flow Init

Configure git-flow for this repository.

## Steps

### 1. Check Installation

```bash
which git-flow || which git
git flow version 2>/dev/null || echo "git-flow not installed"
```

### 2. Initialize

```bash
git flow init -d  # -d uses defaults (main/develop)
```

### 3. Verify Configuration

```bash
git config --get-regexp gitflow
```

## Default Branch Names

| Type | Prefix |
|------|--------|
| Production | `main` |
| Development | `develop` |
| Feature | `feature/` |
| Release | `release/` |
| Hotfix | `hotfix/` |

## Installation (if missing)

**macOS:** `brew install git-flow`
**Fedora:** `sudo dnf install gitflow`
**Ubuntu:** `sudo apt install git-flow`

For git-flow-next (Go version): <https://git-flow.sh/>

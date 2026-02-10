---
name: finish
description: Complete current git-flow branch (feature, release, or hotfix)
allowed-tools:
  - Bash(git *)
  - Bash(pwd)
  - AskUserQuestion
---

# Finish Branch

Complete the current git-flow branch.

## Usage

```text
/gitmastery:finish        # Auto-detect branch type
/gitmastery:finish --tag  # For release/hotfix with tag
```

## Workflow

### 1. Detect Context

```bash
git branch --show-current
git status --short
```

### 2. Execute Based on Type

**Feature/Bugfix:**

```bash
git flow finish  # Merges to develop, deletes branch
```

**Release/Hotfix:**

```bash
git flow finish --no-verify --tag -m "v<version> - Release notes"
```

> **Note:** `--no-verify` skips pre-commit hooks on the merge commit. This is safe because the merge is mechanical — all code was already validated when committed to the release branch.

### 3. Push Changes

```bash
git push origin develop
git push origin main --tags  # For release/hotfix
```

## Branch Actions

| Branch Type | Finish Action |
|-------------|---------------|
| feature/* | Merge to develop |
| bugfix/* | Merge to develop |
| release/* | Merge to main + develop, create tag |
| hotfix/* | Merge to main + develop, create tag |

## Pre-finish Checklist

Present via AskUserQuestion:

- [ ] All tests pass
- [ ] Changelog updated
- [ ] No uncommitted changes
- [ ] Ready to merge

## Conflict Resolution

If conflicts occur:

1. Resolve manually
2. `git add <resolved-files>`
3. `git flow finish` (retry)

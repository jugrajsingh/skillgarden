---
name: finish
description: Complete current git-flow branch (feature, release, or hotfix)
allowed-tools:
  - Bash(git *)
  - Bash(pwd)
  - Bash(SKIP=* git *)
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
SKIP=no-commit-to-branch,conventional-pre-commit git flow finish --tag -m "v<version> - Release notes"
```

> **Note:** The `SKIP` env var bypasses pre-commit hooks that would reject the merge commit. This is safe because:
>
> - The merge is mechanical (no new code changes)
> - All code was already validated when committed to the release branch
> - The `no-commit-to-branch` hook blocks commits to main/develop
> - The `conventional-pre-commit` hook may reject merge commit messages

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

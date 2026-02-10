---
name: release
description: Create a versioned release with semantic versioning
allowed-tools:
  - Bash(git *)
  - Bash(pwd)
  - Bash(SKIP=* git *)
  - Read
  - Edit
  - Glob
  - AskUserQuestion
---

# Create Release

Start or finish a release with semantic versioning.

## Usage

```text
/gitmastery:release         # Analyze and suggest version
/gitmastery:release 1.3.0   # Specific version
```

## Workflow

### 1. Analyze Commits

```bash
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null)
echo "Last tag: $LAST_TAG"
git log $LAST_TAG..HEAD --oneline
```

### 2. Determine Version Bump

| Pattern | Bump | Example |
|---------|------|---------|
| BREAKING or ! suffix | MAJOR | 1.2.3 → 2.0.0 |
| feat: | MINOR | 1.2.3 → 1.3.0 |
| fix:, perf: | PATCH | 1.2.3 → 1.2.4 |

### 3. Present Options

```yaml
AskUserQuestion:
  question: |
    Ready to create release?

    Current: v1.2.1
    Commits: 6 since last release

    Changes detected:
    - 2 feat: (new features)
    - 3 fix: (bug fixes)
    - 1 docs: (documentation)

    Suggested: 1.3.0 (MINOR)

  options:
    - "1.3.0 (Recommended)" - MINOR
    - "2.0.0" - MAJOR
    - "1.2.2" - PATCH
```

### 4. Start Release

```bash
git flow release start <version>
```

### 5. Update Version Files

Common files to update:

- `pyproject.toml`: `version = "<version>"`
- `package.json`: `"version": "<version>"`
- `CHANGELOG.md`: Add version header

### 6. Finish Release

Use changelog content for tag message. Skip pre-commit hooks that would reject the merge:

```bash
SKIP=no-commit-to-branch,conventional-commit git flow finish --tag -m "v<version>

## Added
- Feature 1
- Feature 2

## Fixed
- Bug fix 1"
```

> **Why SKIP?** The merge commit is mechanical—all code was already validated when committed to the release branch. The `no-commit-to-branch` and `conventional-commit` hooks would otherwise reject the merge.

### 7. Push

```bash
git push origin main --tags
git push origin develop
```

## Hotfix Flow

For urgent production fixes:

```bash
git checkout main
git flow hotfix start <name>
# ... fix ...
SKIP=no-commit-to-branch,conventional-commit git flow finish --tag
```

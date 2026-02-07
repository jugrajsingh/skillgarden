---
name: feature
description: Start a new feature branch using git-flow
allowed-tools:
  - Bash(git *)
  - Bash(pwd)
  - AskUserQuestion
---

# Start Feature Branch

## Usage

```text
/gitmastery:feature           # Prompts for name
/gitmastery:feature user-auth # Direct name
```

## Workflow

### 1. Check Current State

```bash
git branch --show-current
git status --short
```

### 2. Switch to Develop if Needed

```bash
git checkout develop
git pull origin develop
```

### 3. Start Feature

```bash
git flow feature start <name>
```

## Naming Convention

```text
<ticket>-<short-description>
```

Examples:

- `PROJ-123-user-authentication`
- `fix-memory-leak`
- `add-export-feature`

## After Starting

You're now on `feature/<name>`. Use:

- `/gitmastery:commit` to commit changes
- `/gitmastery:finish` when complete

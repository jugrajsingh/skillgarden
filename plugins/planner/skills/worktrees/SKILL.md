---
name: worktrees
description: Use when starting isolated development on a branch and need a git worktree with auto-detected project setup and baseline test verification
allowed-tools:
  - Bash(git *)
  - Bash(cd *)
  - Bash(pwd)
  - Bash(ls *)
  - Read
  - Glob
  - AskUserQuestion
---

# Git Worktree Isolation

Set up an isolated git worktree for a branch or task, auto-detect project setup, and run baseline tests.

## Input

`$ARGUMENTS` = branch name or task slug.

If `$ARGUMENTS` is empty, ask:

```yaml
AskUserQuestion:
  question: "What branch name should I create the worktree for?"
  header: "Branch Name"
```

## Step 1: Check Branch State

Check if the branch already exists:

```bash
git branch --list {BRANCH_NAME}
git branch -r --list "origin/{BRANCH_NAME}"
```

If the branch does not exist, confirm creation:

```yaml
AskUserQuestion:
  question: "Branch '{BRANCH_NAME}' doesn't exist. Create it?"
  header: "New Branch"
  options:
    - label: "Yes, create from current HEAD"
      description: "New branch based on current position"
    - label: "Yes, create from develop"
      description: "New branch based on develop"
    - label: "Cancel"
      description: "Don't create the worktree"
```

If "Cancel", exit with no changes.

## Step 2: Detect Worktree Directory

Check for existing worktree directory conventions:

```bash
test -d .worktrees && echo ".worktrees exists"
test -d worktrees && echo "worktrees exists"
```

If neither exists, ask:

```yaml
AskUserQuestion:
  question: "Where should worktrees be stored?"
  header: "Worktree Directory"
  options:
    - label: ".worktrees/ (hidden, recommended)"
      description: "Hidden directory, keeps project root clean"
    - label: "worktrees/"
      description: "Visible directory in project root"
    - label: "Custom path"
      description: "Specify a different location"
```

If "Custom path" is selected, ask for the path.

Ensure the directory is in .gitignore:

```bash
grep -q "{WORKTREE_DIR}" .gitignore 2>/dev/null || echo "{WORKTREE_DIR}/" >> .gitignore
```

## Step 3: Create Worktree

If creating a new branch:

```bash
git worktree add {WORKTREE_DIR}/{BRANCH_NAME} -b {BRANCH_NAME}
```

Or from a specific base:

```bash
git worktree add {WORKTREE_DIR}/{BRANCH_NAME} -b {BRANCH_NAME} develop
```

If the branch already exists:

```bash
git worktree add {WORKTREE_DIR}/{BRANCH_NAME} {BRANCH_NAME}
```

Verify creation:

```bash
git worktree list
```

If the worktree already exists at that path, report it and skip creation.

## Step 4: Auto-Detect and Run Project Setup

Check for manifest files (package.json, pyproject.toml, Cargo.toml, go.mod) and run appropriate setup command. See references/setup-detection.md for manifest-to-command mapping.

## Step 5: Run Baseline Tests

Detect test runner from project manifests and run tests. Report pass/fail counts to establish baseline. See references/setup-detection.md for test runner detection table.

## Step 6: Report

Print branch name, location, setup result, and test results. Include cd and removal commands. See references/setup-detection.md for report template.

## Rules

- Never force-create over an existing worktree
- Always verify worktree creation with `git worktree list`
- Always run tests for baseline when a test runner is available
- Report the exact path for the user to cd into
- Ensure the worktree directory is gitignored
- If branch already exists remotely but not locally, track it: `git worktree add {PATH} -b {NAME} origin/{NAME}`

---
name: worktrees
description: Git worktree isolation — create worktree, detect project setup, run baseline tests
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

Check for manifest files in the worktree:

```bash
ls {WORKTREE_DIR}/{BRANCH_NAME}/package.json {WORKTREE_DIR}/{BRANCH_NAME}/pyproject.toml {WORKTREE_DIR}/{BRANCH_NAME}/Cargo.toml {WORKTREE_DIR}/{BRANCH_NAME}/go.mod 2>/dev/null
```

Run the appropriate setup based on what is found:

| Manifest | Setup Command |
|----------|--------------|
| package.json | `cd {WORKTREE_PATH} && npm install` |
| pyproject.toml | `cd {WORKTREE_PATH} && pip install -e .` |
| Cargo.toml | `cd {WORKTREE_PATH} && cargo build` |
| go.mod | `cd {WORKTREE_PATH} && go mod download` |
| requirements.txt | `cd {WORKTREE_PATH} && pip install -r requirements.txt` |

If no manifest found, report: "No package manifest detected. Skipping auto-setup."

If setup fails, report the error but continue — the worktree is still usable.

## Step 5: Run Baseline Tests

Detect the test runner from the project:

| Indicator | Test Command |
|-----------|-------------|
| pyproject.toml with pytest | `cd {WORKTREE_PATH} && pytest --tb=short -q` |
| package.json with test script | `cd {WORKTREE_PATH} && npm test` |
| Cargo.toml | `cd {WORKTREE_PATH} && cargo test` |
| go.mod | `cd {WORKTREE_PATH} && go test ./...` |

Run tests and capture the result. Report pass/fail counts.

If tests fail, report which tests failed — this establishes the baseline so new failures can be distinguished.

If no test runner detected, report: "No test runner detected. Skipping baseline tests."

## Step 6: Report

```text
## Worktree Ready

Branch:   {BRANCH_NAME}
Location: {WORKTREE_DIR}/{BRANCH_NAME}
Setup:    {setup result or "skipped"}
Tests:    {pass}/{total} passing ({fail} failures)

To work in the worktree:
  cd {WORKTREE_DIR}/{BRANCH_NAME}

To remove later:
  git worktree remove {WORKTREE_DIR}/{BRANCH_NAME}
```

## Rules

- Never force-create over an existing worktree
- Always verify worktree creation with `git worktree list`
- Always run tests for baseline when a test runner is available
- Report the exact path for the user to cd into
- Ensure the worktree directory is gitignored
- If branch already exists remotely but not locally, track it: `git worktree add {PATH} -b {NAME} origin/{NAME}`

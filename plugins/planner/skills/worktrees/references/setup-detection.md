# Project Setup Detection and Baseline Tests

## Auto-Detect Manifest

Check for manifest files in the worktree:

```bash
ls {WORKTREE_PATH}/package.json {WORKTREE_PATH}/pyproject.toml {WORKTREE_PATH}/Cargo.toml {WORKTREE_PATH}/go.mod 2>/dev/null
```

## Setup Commands

| Manifest | Setup Command |
|----------|--------------|
| package.json | `cd {WORKTREE_PATH} && npm install` |
| pyproject.toml | `cd {WORKTREE_PATH} && pip install -e .` |
| Cargo.toml | `cd {WORKTREE_PATH} && cargo build` |
| go.mod | `cd {WORKTREE_PATH} && go mod download` |
| requirements.txt | `cd {WORKTREE_PATH} && pip install -r requirements.txt` |

If no manifest found, report: "No package manifest detected. Skipping auto-setup."
If setup fails, report the error but continue.

## Test Runner Detection

| Indicator | Test Command |
|-----------|-------------|
| pyproject.toml with pytest | `cd {WORKTREE_PATH} && pytest --tb=short -q` |
| package.json with test script | `cd {WORKTREE_PATH} && npm test` |
| Cargo.toml | `cd {WORKTREE_PATH} && cargo test` |
| go.mod | `cd {WORKTREE_PATH} && go test ./...` |

Run tests and capture pass/fail counts. Report which tests failed to establish baseline.
If no test runner detected, report: "No test runner detected. Skipping baseline tests."

## Report Template

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

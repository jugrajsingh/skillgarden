---
name: commit
description: Create atomic git commits with conventional format. Hooks enforce no wildcards, no AI footers, conventional format.
---

# Atomic Commit Workflow

Create atomic commits with conventional format. **Hooks auto-validate all commands.**

## Critical Rules

| Rule | Enforcement |
|------|-------------|
| No wildcards | Hook rejects `*`, `.`, `-A` |
| No AI footers | Hook rejects `Co-Authored-By: Claude` |
| Conventional format | Hook validates `type(scope): subject` |
| Separate commands | Never chain with `&&` |

## Workflow

### 1. Verify State

```bash
pwd
git status --short
git diff --cached --name-only
```

If files staged: `git reset HEAD` to unstage first.

### 2. Analyze Changes

```bash
git diff --stat
git log -3 --oneline
```

### 3. Group Logically

Separate commits for:

- **feat** ↔ **test** (feature code vs tests)
- **feat** ↔ **refactor** (new vs restructure)
- **code** ↔ **docs** (implementation vs documentation)
- **code** ↔ **chore** (changes vs config)

Atomic = one logical change, buildable, reversible.

### 4. For Each Commit

**a) Present via AskUserQuestion:**

```text
Ready to create commit 1/N?

**Commit Message:**
feat(auth): add JWT refresh endpoint

Implements automatic token refresh 5 minutes before expiry.
Tokens are refreshed in background to avoid request delays.

**Files:**
- src/auth.py (+45/-3)
- src/tokens.py (+30)

**Stats:** 2 files, +75/-3

**Commands:**
1. git add src/auth.py src/tokens.py
2. pre-commit run
3. git commit -m "feat(auth): add JWT refresh endpoint

Implements automatic token refresh 5 minutes before expiry.
Tokens are refreshed in background to avoid request delays."
```

**b) Execute ONE command at a time:**

```bash
# Step 1: Stage (hook validates)
git add src/auth.py src/tokens.py

# Step 2: Pre-commit (retry if auto-fixed)
pre-commit run

# Step 3: Commit ONLY if hooks pass
git commit -m "feat(auth): add JWT refresh endpoint

Implements automatic token refresh 5 minutes before expiry."
```

### 5. Pre-commit Handling

| Exit Code | Action |
|-----------|--------|
| 0 | Proceed to commit |
| Non-zero + files modified | Re-stage same files, retry |
| Non-zero + error | Show error, ask user |

Auto-fixable: `ruff-format`, `trailing-whitespace`, `end-of-file-fixer`

Retry loop:

```bash
git add file1.py file2.py  # Re-stage
pre-commit run             # Retry
# If pass → commit
```

### 6. Submodule Handling

When `git status` shows `modified: submodule (modified content)`:

**Step 1: Enter submodule (separate command):**

```bash
cd submodule
```

```bash
pwd  # Verify
```

**Step 2: Commit inside:**

```bash
git status
git add file.py
pre-commit run
git commit -m "feat: change description"
```

**Step 3: Return to root:**

```bash
cd ..
```

```bash
pwd  # Verify
```

**Step 4: Update reference:**

```bash
git add submodule
git commit -m "chore(submodule): update reference"
```

**CRITICAL:** Never chain `cd` with other commands.

### 7. Summary Report

```text
## Commits Created

1. `abc1234` feat(auth): add JWT refresh endpoint
   - 2 files, +75/-3
   - Pre-commit: Passed

2. `def5678` test(auth): add refresh token tests
   - 1 file, +120
   - Pre-commit: Passed (2 retries)

Total: 2 commits | 3 files | +195/-3
```

## Commit Message Format

```text
<type>(<scope>): <subject>

<body - explain what and why>

<footer - BREAKING CHANGE: or Fixes #123>
```

| Part | Rule |
|------|------|
| Subject | Imperative, lowercase, no period, ≤50 chars |
| Body | Wrap at 72 chars, explain what/why |
| Footer | `BREAKING CHANGE:` or `Fixes #123` |

**Types:**

| Type | Use For |
|------|---------|
| feat | New feature |
| fix | Bug fix |
| docs | Documentation only |
| style | Formatting (no logic change) |
| refactor | Code restructure (no behavior change) |
| test | Adding/fixing tests |
| chore | Maintenance, deps, config |
| perf | Performance improvement |
| ci | CI/CD changes |
| build | Build system changes |

## Anti-Patterns (Blocked by Hooks)

```bash
# WRONG: Wildcards
git add *.py          # Hook blocks

# WRONG: Current directory
git add .             # Hook blocks

# WRONG: All flag
git add -A            # Hook blocks

# WRONG: AI footer
git commit -m "feat: add feature

Co-Authored-By: Claude"  # Hook blocks

# WRONG: Bad format
git commit -m "added feature"  # Hook blocks

# WRONG: Chained commands
git add file.py && pre-commit run  # Avoid
```

---
name: shipping
description: Branch completion — pre-ship checks, 4-option choice (merge, PR, keep, discard), cleanup
---

# Ship Branch

Complete the current branch with pre-ship checks and one of four completion options.

## Input

$ARGUMENTS = optional action: merge, pr, keep, or discard.

If $ARGUMENTS is empty, present all 4 options after pre-ship checks.

## Step 1: Pre-Ship Checks

Run these checks and report results:

**1. Uncommitted changes:**

```bash
git status --short
```

Record: clean or list of uncommitted files.

**2. Test suite:**
Run the project's test suite (detect runner from project files: pytest, npm test, cargo test, go test).
Record: pass/fail with counts.

**3. Review status:**
Check for review report matching current branch:

```bash
git branch --show-current
```

Then check docs/reviews/ for a matching review file.
Record: reviewed or not reviewed.

**4. Current branch:**

```bash
git branch --show-current
```

Verify we are on a feature, bugfix, release, or hotfix branch. If on main or develop, warn: "Cannot ship from {branch}. Switch to a feature branch first."

**Report check results:**

```text
## Pre-Ship Checks

| Check | Status |
|-------|--------|
| Uncommitted changes | {clean / N files} |
| Test suite | {pass / fail} |
| Code review | {reviewed / not reviewed} |
| Branch | {branch_name} |
```

If uncommitted changes exist or tests fail:

- Warn the user with specifics
- Ask via AskUserQuestion: "Proceed anyway" or "Fix issues first"
- If user chooses to fix, stop and let them handle it

## Step 2: Choose Action

If $ARGUMENTS specified an action, use it directly.

Otherwise, present options via AskUserQuestion:

- "Merge locally" — merge to parent branch via git-flow, delete feature branch
- "Create PR" — push branch and create a pull request
- "Keep branch" — leave as-is for later
- "Discard branch" — delete branch and all changes (requires confirmation)

## Step 3: Execute Action

### Option: Merge Locally

1. Load the `gitmastery:finish` skill
   - This handles git flow finish: merge to parent branch, delete feature branch
   - Follow the skill's workflow exactly

2. After merge completes, check if remote tracking exists:

   ```bash
   git rev-parse --abbrev-ref --symbolic-full-name @{upstream} 2>/dev/null
   ```

   If remote tracking exists, push the parent branch:

   ```bash
   git push origin {parent_branch}
   ```

3. Report: "Branch merged to {parent_branch} and pushed."

### Option: Create PR

1. Push the branch to remote:

   ```bash
   git push -u origin {branch_name}
   ```

2. Load the `shipit:describing-pr` skill for PR description generation and creation

3. Report the PR URL when complete

### Option: Keep Branch

1. Report:

   ```text
   Branch {branch_name} kept.

   Resume options:
   - /shipit:execute {slug} — continue executing tasks
   - /shipit:ship — return to shipping options
   ```

2. No changes made. Branch stays as-is.

### Option: Discard Branch

1. Require explicit confirmation via AskUserQuestion:
   "Type the branch name to confirm deletion: {branch_name}"

2. Verify the typed name matches the current branch exactly. If it does not match:
   - Report: "Branch name does not match. Deletion cancelled."
   - Stop.

3. Switch to develop:

   ```bash
   git checkout develop
   ```

4. Delete the branch:

   ```bash
   git branch -D {branch_name}
   ```

5. If a remote branch exists, delete it:

   ```bash
   git push origin --delete {branch_name} 2>/dev/null
   ```

6. Report: "Branch {branch_name} deleted locally and remotely."

## Step 4: Cleanup

For merge, PR, and discard actions:

1. Check if a worktree exists for this branch:

   ```bash
   git worktree list
   ```

   If a worktree is found for the branch:

   ```bash
   git worktree remove {worktree_path}
   ```

2. Report final state:

   ```text
   ## Ship Complete

   Action: {merge/pr/keep/discard}
   Branch: {branch_name}
   Result: {description of what happened}
   Current branch: {where we are now}
   ```

## Rules

- Always run pre-ship checks before any action
- Never force-delete without explicit user confirmation (typed branch name)
- Merge delegates to gitmastery:finish — do not implement merge logic directly
- PR creation delegates to shipit:describing-pr — do not implement PR logic directly
- If on main or develop, refuse to ship and explain why
- Warn on uncommitted changes or failing tests, but let user override

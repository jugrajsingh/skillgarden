---
name: describing-pr
description: Generate PR description from changes and plan context — summary, changes, test plan, breaking changes
allowed-tools:
  - Bash(git *)
  - Bash(gh *)
  - Read
  - Glob
  - Grep
  - AskUserQuestion
---

# Describe PR

Generate a structured PR description from branch changes and plan context, then create the PR.

## Input

$ARGUMENTS = optional base branch. Defaults to develop.

## Step 1: Gather Changes

Run these commands to understand what this PR contains:

**Commit history:**

```bash
git log {base}...HEAD --oneline
```

**File change summary:**

```bash
git diff {base}...HEAD --stat
```

**Full diff for analysis:**

```bash
git diff {base}...HEAD
```

**Current branch:**

```bash
git branch --show-current
```

If the diff is empty (no changes vs base), report "No changes found between {branch} and {base}. Nothing to create a PR for." and stop.

## Step 2: Read Context

**Task plan context:**

- Derive slug from branch name (e.g., feature/add-auth -> add-auth)
- Check docs/plans/{slug}/task_plan.md — if it exists, read it for:
  - Feature description and goals
  - Acceptance criteria
  - Design decisions

**Design docs:**

- Check docs/plans/ for any design documents related to the slug

**Commit message context:**

- Parse commit messages for:
  - Acceptance criteria (lines containing "Acceptance:" or "Criteria:")
  - Breaking change footers (BREAKING CHANGE: or commits with type ending in exclamation mark)
  - Scope information from conventional commit prefixes

## Step 3: Generate PR Description

Build the PR description with these sections:

### Title

Derive from branch name or plan title:

- feature/add-user-auth -> "Add user authentication"
- fix/handle-null-response -> "Fix null response handling"
- Use sentence case, imperative mood

### Summary

1-3 bullet points describing:

- WHAT changed (the feature/fix/refactor)
- WHY it changed (the motivation or problem being solved)
- Draw from task_plan.md goals if available

### Changes

Group changes by type based on commit prefixes:

- **Features**: feat() commits
- **Fixes**: fix() commits
- **Refactors**: refactor() commits
- **Tests**: test() commits
- **Documentation**: docs() commits
- **Chores**: chore() commits

List each change as a bullet point with brief description.

### Test Plan

Derive from acceptance criteria:

- If task_plan.md exists: convert acceptance criteria to checklist items
- If no plan: extract testable claims from commit messages
- Format as bulleted markdown checklist:

  ```text
  - [ ] Criterion 1 description
  - [ ] Criterion 2 description
  ```

### Breaking Changes

Scan for breaking changes:

- Commits with BREAKING CHANGE in the footer
- Commits with type ending in exclamation mark (e.g., feat(api)!: change endpoint)
- If none found, omit this section entirely (do not include "None")

## Step 4: Present Draft

Output the full PR description draft.

Ask via AskUserQuestion:

- "Create PR with this description" — proceed to PR creation
- "Edit description first" — let user modify, then ask again
- "Skip PR creation" — output the description but do not create PR

## Step 5: Create PR

If user chose to create:

1. Ensure branch is pushed:

   ```bash
   git push -u origin {branch_name}
   ```

2. Create the PR using gh CLI with HEREDOC for the body:

   ```bash
   gh pr create --title "{title}" --body "$(cat <<'EOF'
   {full PR body}
   EOF
   )" --base {base}
   ```

3. Capture and report the PR URL.

Output:

```text
## PR Created

URL: {pr_url}
Title: {title}
Base: {base} <- {branch}
```

## Rules

- Always gather actual diff — never generate PR description from memory
- Summary focuses on WHY, not just WHAT
- Test plan must be actionable checklist items, not vague descriptions
- Breaking changes section only appears if breaking changes exist
- PR body uses HEREDOC to preserve formatting in gh command
- If gh CLI is not available, output the description and instruct user to create PR manually
- Title uses sentence case and imperative mood

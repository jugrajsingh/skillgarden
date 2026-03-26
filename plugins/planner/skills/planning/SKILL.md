---
name: planning
description: Use when you have a design doc or feature description and need to break it into discrete, ordered tasks with dependency tracking and batch grouping
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
---

# Implementation Planning

Create implementation plans with task decomposition, dependency ordering, and 3-file persistence for session continuity.

## Input

`$ARGUMENTS` = path to design doc OR feature description text.

If empty: list `docs/plans/*-design.md`, offer selection via AskUserQuestion. If no design docs, ask for feature description directly.

## Step 1: Read and Analyze Source

If `$ARGUMENTS` is a file path, read that file. Otherwise, use the text as the feature description.

Identify:

- All files to create (exact paths)
- All files to modify (exact paths)
- Existing patterns to follow

Scan the codebase for conventions:

```bash
ls -la src/ lib/ app/ 2>/dev/null
```

```bash
git log -10 --oneline
```

Read any referenced files to understand the current structure.

## Step 2: Initialize Persistence Files

Generate a slug from the feature name (lowercase, hyphenated, max 5 words).

```bash
mkdir -p docs/plans/{SLUG}
```

Read templates from `${CLAUDE_PLUGIN_ROOT}/templates/`:

- `${CLAUDE_PLUGIN_ROOT}/templates/task_plan.md`
- `${CLAUDE_PLUGIN_ROOT}/templates/findings.md`
- `${CLAUDE_PLUGIN_ROOT}/templates/progress.md`

Create 3 files, replacing template placeholders:

| File | Path |
|------|------|
| Task Plan | docs/plans/{SLUG}/task_plan.md |
| Findings | docs/plans/{SLUG}/findings.md |
| Progress | docs/plans/{SLUG}/progress.md |

Replace `{TITLE}` with the feature title, `{DATE}` with today's date, `{DESIGN_DOC}` with the source design doc path (or "inline description").

## Step 3: Decompose into Tasks

Break feature into discrete tasks with: ID (T01, T02...), description (imperative verb phrase), files (exact paths), acceptance criteria, TDD test names, and dependencies.

See references/task-format.md for field definitions, example task, and decomposition guidelines.

## Step 4: Research Gaps

For each task, verify referenced files exist, imports are available, and APIs have expected signatures. Record patterns found, open questions, and research notes in `docs/plans/{SLUG}/findings.md`. If significant unknowns, ask user: continue (mark as open) or clarify now.

## Step 5: Order by Dependency and Batch

Sort tasks by dependency order. Group into batches (max 3 tasks per batch, no intra-batch dependencies, batch N+1 depends on batch N). Write to `docs/plans/{SLUG}/task_plan.md`. See references/task-format.md for batching rules and format.

## Step 6: Initialize Progress Tracking

Write `docs/plans/{SLUG}/progress.md` with all tasks set to pending and batch log entries. See references/task-format.md for progress tracking template.

## Step 7: Present Plan Summary

Report feature title, task/batch counts, file counts, open questions, and persistence file paths. Offer: execute now, execute in new session (`/planner:resume {SLUG}`), or refine plan. See references/task-format.md for summary format.

## Rules

- Every task must have at least one acceptance criterion
- Every task must reference exact file paths (no wildcards)
- Batches respect dependencies strictly — never schedule a task before its dependencies
- Maximum 3 tasks per batch
- Test names follow test_should_{behavior}_when_{condition} format
- Findings file is updated during planning, not just at the end
- Keep task_plan.md under 300 lines; use concise descriptions
- Reference persistence-format.md for file schemas

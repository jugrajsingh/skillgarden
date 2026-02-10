---
name: planning
description: Implementation planning with 3-file persistence — task decomposition, dependency ordering, batch grouping
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

If `$ARGUMENTS` is empty:

```bash
ls -t docs/plans/*-design.md 2>/dev/null | head -5
```

If design docs exist, offer selection:

```yaml
AskUserQuestion:
  question: "Which design doc should I plan from?"
  header: "Select Design"
  options:
    - label: "{DESIGN_1}"
      description: "{first line of file}"
    - label: "{DESIGN_2}"
      description: "{first line of file}"
    - label: "Describe a feature instead"
      description: "I'll provide a feature description directly"
```

If no design docs and no arguments, ask:

```yaml
AskUserQuestion:
  question: "What feature or change should I create a plan for?"
  header: "Feature Description"
```

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
mkdir -p docs/plans
```

Read templates from `${CLAUDE_PLUGIN_ROOT}/templates/`:

- `${CLAUDE_PLUGIN_ROOT}/templates/task_plan.md`
- `${CLAUDE_PLUGIN_ROOT}/templates/findings.md`
- `${CLAUDE_PLUGIN_ROOT}/templates/progress.md`

Create 3 files, replacing template placeholders:

| File | Path |
|------|------|
| Task Plan | `docs/plans/{SLUG}-task_plan.md` |
| Findings | `docs/plans/{SLUG}-findings.md` |
| Progress | `docs/plans/{SLUG}-progress.md` |

Replace `{TITLE}` with the feature title, `{DATE}` with today's date, `{DESIGN_DOC}` with the source design doc path (or "inline description").

## Step 3: Decompose into Tasks

Break the feature into discrete tasks. Each task:

| Field | Format |
|-------|--------|
| ID | T01, T02, T03... |
| Description | Imperative verb phrase (e.g., "Add user validation endpoint") |
| Files | Exact file paths to create or modify |
| Acceptance | At least one measurable criterion |
| TDD | Test name: `test_should_{behavior}_when_{condition}` — assertion description |
| Dependencies | Task IDs that must complete first, or "none" |

Example task:

```text
### T01: Create user validation schema
- Files: src/schemas/user.py, tests/test_schemas/test_user.py
- Acceptance: Schema validates email format, rejects missing required fields
- TDD: test_should_reject_invalid_email_when_format_wrong — assert ValidationError raised with field name
- TDD: test_should_accept_valid_user_when_all_fields_present — assert no error, returns validated model
- Depends: none
```

Guidelines for task decomposition:

- Each task should be completable in one focused session
- Prefer smaller tasks over larger ones
- Test files are part of the same task as implementation (TDD)
- Configuration/setup tasks come first
- Integration tasks come last

## Step 4: Research Gaps

For each task, verify:

1. Referenced files exist (or are being created by a prior task)
2. Imports and dependencies are available
3. APIs being called actually exist with expected signatures

```bash
test -f {FILE_PATH} && echo "exists" || echo "missing"
```

Record findings in `docs/plans/{SLUG}-findings.md`:

- **Patterns Found**: Conventions discovered in the codebase (e.g., "all endpoints follow router pattern in src/routes/")
- **Open Questions**: Things that need clarification (mark as open)
- **Research Notes**: Timestamped notes from investigation

If significant unknowns exist, flag them:

```yaml
AskUserQuestion:
  question: "I found gaps that may need research. How should I proceed?"
  header: "Research Gaps"
  options:
    - label: "Continue planning — I'll resolve later"
      description: "Mark gaps as open questions and proceed"
    - label: "Let me clarify now"
      description: "I'll answer your questions before you continue"
```

## Step 5: Order by Dependency and Batch

Sort tasks by dependency order. Group into batches:

- Tasks within a batch have no dependencies on each other
- Maximum 3 tasks per batch
- Batch N+1 depends on at least one task in batch N

Write to `docs/plans/{SLUG}-task_plan.md`:

```markdown
## Batches

### Batch 1
- T01: {description} (no dependencies)
- T03: {description} (no dependencies)

### Batch 2
- T02: {description} (depends on T01)
- T04: {description} (depends on T03)

### Batch 3
- T05: {description} (depends on T02, T04)
```

## Step 6: Initialize Progress Tracking

Write `docs/plans/{SLUG}-progress.md` with all tasks set to pending:

```markdown
## Status

| Task | Status | Notes |
|------|--------|-------|
| T01 | pending | -- |
| T02 | pending | -- |
| T03 | pending | -- |

## Batch Log

### Batch 1 -- not started
Started: --
Completed: --
Notes: --

### Batch 2 -- not started
Started: --
Completed: --
Notes: --
```

## Step 7: Present Plan Summary

Report:

```text
## Plan Summary

Feature: {TITLE}
Tasks: {N} total across {M} batches
Files: {X} to create, {Y} to modify
Open Questions: {Q}

Persistence:
- Task Plan: docs/plans/{SLUG}-task_plan.md
- Findings:  docs/plans/{SLUG}-findings.md
- Progress:  docs/plans/{SLUG}-progress.md
```

Offer next action:

```yaml
AskUserQuestion:
  question: "Plan is ready. What next?"
  header: "Next Action"
  options:
    - label: "Execute now"
      description: "Start implementing Batch 1 immediately"
    - label: "Execute in new session"
      description: "Save plan and use /planner:resume to pick up later"
    - label: "Refine plan"
      description: "Adjust tasks, dependencies, or batching"
```

- "Execute now" — report: "Run /planner:resume {SLUG} in this or a new session to begin execution."
- "Execute in new session" — report persistence file paths and suggest: "Run /planner:resume {SLUG} to recover context."
- "Refine plan" — ask what to change and iterate on Steps 3-6

## Rules

- Every task must have at least one acceptance criterion
- Every task must reference exact file paths (no wildcards)
- Batches respect dependencies strictly — never schedule a task before its dependencies
- Maximum 3 tasks per batch
- Test names follow test_should_{behavior}_when_{condition} format
- Findings file is updated during planning, not just at the end
- Keep task_plan.md under 300 lines; use concise descriptions
- Reference persistence-format.md for file schemas

---
name: executing
description: Batch execution with subagent pipeline — load plan, create native Tasks, run implement-review pipeline per batch
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Task
  - AskUserQuestion
---

# Batch Execution Pipeline

Execute tasks from a plan using a 3-stage subagent pipeline per task with native Task coordination.

## Input

$ARGUMENTS = path to task_plan.md or slug.

If $ARGUMENTS is empty:

1. Check docs/plans/ for task plan files
2. If multiple plans found, present list via AskUserQuestion and let user select
3. If no plans found, report error: "No task plans found in docs/plans/. Create one with /planner:plan first."

## Step 1: Load Plan and Progress

1. Read the task_plan.md file (resolve slug to docs/plans/{slug}/task_plan.md if needed)
2. Check for progress.md in the same directory
3. If progress.md exists, parse it to find the next incomplete batch (first batch with tasks not marked "done")
4. If no progress.md, initialize one from task_plan.md and start from Batch 1
5. Report: "Resuming from Batch {N}" or "Starting from Batch 1"

## Step 2: Create Native Tasks for Current Batch

For each task in the current batch, create three native Tasks using TaskCreate:

1. **Implementation Task**
   - subject: "Implement {TASK_ID}: {task description}"
   - activeForm: "Implementing {TASK_ID}"
   - No blockers

2. **Spec Review Task**
   - subject: "Spec-review {TASK_ID}: verify implementation matches requirements"
   - blockedBy: implementation task ID

3. **Quality Review Task**
   - subject: "Quality-review {TASK_ID}: check code quality and conventions"
   - blockedBy: spec-review task ID

This creates a dependency chain: Implement -> Spec Review -> Quality Review

## Step 3: Execute Pipeline Per Task

For each task in the batch, run the 3-stage pipeline sequentially.

### Stage 1 — Implement

Spawn a Task agent (subagent_type: general-purpose) with implementer instructions.

Provide the agent with:

- Task ID and description from the plan
- File paths to create or modify
- Acceptance criteria for this task
- TDD steps: test name (test_should_{behavior}_when_{condition}), what to assert
- Plan context: how this task fits the larger feature

Agent instructions:

- Follow RED-GREEN-REFACTOR strictly
- RED: write failing test, run it, confirm it fails for the right reason
- GREEN: write minimal code to make the test pass, run tests
- REFACTOR: improve code quality while keeping tests green
- Commit after green using conventional format (explicit file paths, no wildcards, no AI footers)
- Report: what was implemented, test results, files changed, any concerns

When agent completes, update the native Task status to completed.

If implementation fails (tests won't pass after reasonable attempts):

- Retry once with adjusted approach
- If still failing, mark task as blocked and flag for user attention
- Do NOT proceed to spec review for this task

### Stage 2 — Spec Review

Only runs after Stage 1 completes successfully.

Spawn a Task agent (subagent_type: general-purpose, model: sonnet) with spec-reviewer instructions.

Provide the agent with:

- Task requirements: description, acceptance criteria from task_plan.md
- Implementer's report: what they claim to have done
- Changed files list from the implementation

Agent instructions:

- Read the actual code independently — NEVER trust the implementer's report at face value
- For each acceptance criterion, verify it is met by reading the code
- Check test quality: do tests actually test what they claim?
- Every finding must include file:line reference
- Report: PASS or FAIL verdict with specific deviations

When agent completes, update the native Task status.

If spec review FAILS:

- Flag the task for user attention with specific deviations
- Do NOT proceed to quality review
- Present failure details and ask user how to proceed via AskUserQuestion:
  - "Fix deviations and re-run pipeline for this task"
  - "Skip this task and continue batch"
  - "Abort batch"

### Stage 3 — Quality Review

Only runs if spec review PASSES.

Spawn a Task agent (subagent_type: general-purpose, model: sonnet) with quality-reviewer instructions.

Provide the agent with:

- Changed files list
- Project conventions (from CLAUDE.md if present)
- Spec review result confirming PASS

Agent instructions:

- Check SOLID compliance (SRP, OCP, LSP, ISP, DIP)
- Check error handling (specific exceptions, logger.exception in except blocks)
- Check test coverage gaps (missing edge cases, error paths)
- Check project conventions (naming, imports, type annotations, docstrings)
- Report findings with severity: minor (diamond open), major (diamond filled), critical (double diamond filled)

Severity symbols:

- Minor issues use the open diamond symbol
- Major issues use the filled diamond symbol
- Critical issues use double filled diamond symbols

When agent completes, update the native Task status.

If critical findings exist:

- Flag for user attention with specific findings
- Suggest fixes before proceeding to next batch
- Present via AskUserQuestion: "Address critical issues now" or "Acknowledge and continue"

## Step 4: Batch Checkpoint

After all tasks in the current batch complete (or are flagged):

1. Mirror native Task statuses to progress.md:
   - Update the Status table for each task in the batch
   - Record: task ID, status (done/blocked/skipped), review verdicts, notes

2. Log batch completion in progress.md Batch Log section:

   ```text
   ### Batch {N} — {DATE}
   - Tasks completed: {N}/{total}
   - Spec reviews: {pass_count} pass, {fail_count} fail
   - Quality findings: {critical} critical, {major} major, {minor} minor
   ```

3. Present batch checkpoint via AskUserQuestion with three options:
   - "Continue to next batch" — proceed to Step 2 with next batch
   - "Pause execution" — save state to progress.md, report resume instructions. User can resume later with /shipit:execute {slug}
   - "Abort" — save state, mark remaining tasks as skipped in progress.md

## Step 5: Final Verification

After all batches complete:

1. Load the `shipit:verifying` skill for final verification against the full plan's acceptance criteria
2. Report overall execution summary:

```text
## Execution Complete

Plan: {slug}
Batches: {completed}/{total}
Tasks: {done}/{total} ({blocked} blocked, {skipped} skipped)

### Review Summary
- Spec reviews: {pass}/{total}
- Quality findings: {critical} critical, {major} major, {minor} minor

### Verification
{ result from verifying skill }

### Next Steps
{ recommend /shipit:ship if verification passes }
{ recommend fixing issues if verification fails }
```

## Rules

- Fresh agent per task — no shared context between task agents. Each agent receives only what it needs
- Never skip TDD — implementation agents must follow RED-GREEN-REFACTOR
- Native Tasks for real-time coordination — use TaskCreate, TaskUpdate for status tracking
- progress.md for persistence — all state survives session interruption
- Stop on blocker — critical quality finding or spec failure blocks the batch until user decides
- Each commit follows conventional format — type(scope): subject, no AI footers, explicit file paths
- Refer to `references/batch-protocol.md` for detailed pipeline and failure handling protocol

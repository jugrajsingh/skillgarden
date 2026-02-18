# Pipeline Stage Details

## Stage 1 — Implement

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

## Stage 2 — Spec Review

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

## Stage 3 — Quality Review

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

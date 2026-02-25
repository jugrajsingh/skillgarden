# Task Decomposition Format and Batching

## Task Fields

| Field | Format |
|-------|--------|
| ID | T01, T02, T03... |
| Description | Imperative verb phrase (e.g., "Add user validation endpoint") |
| Files | Exact file paths to create or modify |
| Acceptance | At least one measurable criterion |
| TDD | Test name: `test_should_{behavior}_when_{condition}` — assertion description |
| Dependencies | Task IDs that must complete first, or "none" |

## Example Task

```text
### T01: Create user validation schema
- Files: src/schemas/user.py, tests/test_schemas/test_user.py
- Acceptance: Schema validates email format, rejects missing required fields
- TDD: test_should_reject_invalid_email_when_format_wrong — assert ValidationError raised with field name
- TDD: test_should_accept_valid_user_when_all_fields_present — assert no error, returns validated model
- Depends: none
```

## Guidelines

- Each task completable in one focused session
- Prefer smaller tasks over larger ones
- Test files are part of the same task as implementation (TDD)
- Configuration/setup tasks come first
- Integration tasks come last

## Batching Rules

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

## Progress Tracking Template

Write `docs/plans/{SLUG}-progress.md`:

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

## Plan Summary Format

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

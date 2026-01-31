---
name: persistence-format
description: Schema reference for the 3-file persistence system used by planner skills
---

# 3-File Persistence Format

The planner uses three files in docs/plans/ to maintain state across sessions.

## task_plan.md

```markdown
# Task Plan: {TITLE}

**Created:** {DATE}
**Design:** {DESIGN_DOC_PATH}
**Status:** draft | active | complete

## Tasks

### T01: {description}
- Files: {exact/file/paths}
- Acceptance: {measurable criterion}
- TDD: {test_should_behavior_when_condition} -- {assertion description}
- Depends: none

### T02: {description}
- Files: {exact/file/paths}
- Acceptance: {criterion 1}; {criterion 2}
- TDD: {test_name_1} -- {assertion}
- TDD: {test_name_2} -- {assertion}
- Depends: T01

## Batches

### Batch 1
- T01, T03 (independent)

### Batch 2
- T02 (depends on T01)

### Batch 3
- T04 (depends on T02, T03)
```

## findings.md

```markdown
# Findings: {TITLE}

**Updated:** {DATE}

## Patterns Found

- {pattern description}: {file:line or file reference}
- {convention}: {example location}

## Open Questions

- {question} -- status: open
- {resolved question} -- status: resolved -- {answer}

## Research Notes

- {YYYY-MM-DD}: {investigation note}
- {YYYY-MM-DD}: {discovery or decision}
```

## progress.md

```markdown
# Progress: {TITLE}

**Updated:** {DATE}

## Status

| Task | Status | Notes |
|------|--------|-------|
| T01 | pending | -- |
| T02 | in-progress | started implementation |
| T03 | done | tests passing |
| T04 | blocked | waiting on T02 |

Valid statuses: pending, in-progress, done, blocked, skipped

## Batch Log

### Batch 1 -- complete
Started: {DATE}
Completed: {DATE}
Notes: All tasks passed tests

### Batch 2 -- in-progress
Started: {DATE}
Completed: --
Notes: T02 implementation underway

### Batch 3 -- not started
Started: --
Completed: --
Notes: --
```

## Naming Convention

All three files share the same slug prefix:

- `{SLUG}-task_plan.md`
- `{SLUG}-findings.md`
- `{SLUG}-progress.md`

Slug format: lowercase, hyphenated, max 5 words. Derived from feature name.

Example: feature "Add JWT refresh endpoint" becomes slug `jwt-refresh-endpoint`.

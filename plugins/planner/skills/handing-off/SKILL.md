---
name: handing-off
description: Generate session transfer document — decisions, open questions, blockers, next steps for the next session
---

# Session Handoff

Generate a structured transfer document so the next session can pick up with full context.

## Input

`$ARGUMENTS` = optional slug name.

If `$ARGUMENTS` is empty, find the most recently modified plan:

```bash
ls -t docs/plans/*-progress.md 2>/dev/null | head -3
```

If multiple found, offer selection. If none found, report: "No plan files found. Use /planner:plan to create one."

## Step 1: Read All Context

Read the persistence files for the slug:

- `docs/plans/{SLUG}-task_plan.md`
- `docs/plans/{SLUG}-findings.md`
- `docs/plans/{SLUG}-progress.md`

Also check for related research:

```bash
ls docs/research/ 2>/dev/null | head -10
```

Read any research files that relate to the slug or feature name.

Read recent commit messages for decisions captured in code:

```bash
git log -10 --oneline
```

## Step 2: Gather Handoff Data

Extract from the persistence files:

**Decisions Made** (from findings.md resolved items + commit messages):

- Find all entries in findings.md marked "status: resolved"
- Extract relevant commit messages that indicate design choices
- Include the rationale for each decision

**Open Questions** (from findings.md open items):

- Find all entries marked "status: open"
- Note which tasks they affect

**Blockers** (from progress.md):

- Find tasks with status "blocked" and their notes
- Find tasks with status "in-progress" that have stalled (no recent batch log updates)

**Next Steps** (from task_plan.md):

- Identify the next incomplete batch
- List specific task IDs and their descriptions
- Note dependencies that must be satisfied

## Step 3: Read Handoff Template

```bash
cat ${CLAUDE_PLUGIN_ROOT}/templates/handoff.md
```

## Step 4: Generate Handoff Document

Create `docs/plans/{SLUG}-handoff.md`:

```markdown
# Handoff: {TITLE}

**Date:** {TODAY}
**Plan:** docs/plans/{SLUG}-task_plan.md

## Context

{ 1-2 sentence summary: what the feature is and where it stands }

## Decisions Made

- {decision}: {rationale} (source: {findings.md | commit hash})
- {decision}: {rationale}

## Open Questions

- {question} -- affects: {task IDs}
- {question} -- affects: {task IDs}

## Blockers

- {task ID}: {blocker description}
- {issue}: {what is needed to unblock}

## Next Steps

1. Resume from Batch {N}
2. {task ID}: {description} -- {key context}
3. {task ID}: {description} -- {key context}

## Files of Interest

- {file path} -- {why the next session should read this}
- {file path} -- {contains key pattern or decision}
```

## Step 5: Report

Report:

```text
## Handoff Complete

File: docs/plans/{SLUG}-handoff.md

Summary:
- Decisions: {N} documented
- Open Questions: {N} remaining
- Blockers: {N} active
- Next Batch: {N} with {X} tasks

To resume: /planner:resume {SLUG}
```

## Rules

- Never fabricate decisions — only include what is evidenced in files or commits
- Include specific task IDs in next steps, not vague descriptions
- Files of Interest should be files the next session needs to read first to rebuild context
- Keep the handoff doc under 150 lines
- Always include the /planner:resume command for the next session

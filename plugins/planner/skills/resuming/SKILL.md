---
name: resuming
description: Use when resuming work on a partially-completed plan and need to rebuild session context from persistence files via the 5-Question Reboot Test
allowed-tools:
  - Read
  - Glob
  - AskUserQuestion
---

# Session Recovery

Recover session state by reading persistence files and answering the 5-Question Reboot Test.

## Input

`$ARGUMENTS` = optional slug name.

If `$ARGUMENTS` is empty, find the most recently modified plan files:

```bash
ls -t docs/plans/*-progress.md 2>/dev/null | head -5
```

If multiple found, offer selection:

```yaml
AskUserQuestion:
  question: "Which plan should I resume?"
  header: "Select Plan"
  options:
    - label: "{SLUG_1}"
      description: "Last modified: {date}"
    - label: "{SLUG_2}"
      description: "Last modified: {date}"
```

If none found, report: "No plan files found in docs/plans/. Use /planner:plan to create one."

## Step 1: Locate Persistence Files

Check for all 3 files:

```bash
test -f docs/plans/{SLUG}-task_plan.md && echo "task_plan: found" || echo "task_plan: MISSING"
test -f docs/plans/{SLUG}-findings.md && echo "findings: found" || echo "findings: MISSING"
test -f docs/plans/{SLUG}-progress.md && echo "progress: found" || echo "progress: MISSING"
```

If any file is missing, report which ones and offer:

```yaml
AskUserQuestion:
  question: "Some persistence files are missing. How should I proceed?"
  header: "Missing Files"
  options:
    - label: "Create from template"
      description: "Generate missing files using templates"
    - label: "Continue without"
      description: "Work with available files only"
```

If creating from template, read `${CLAUDE_PLUGIN_ROOT}/templates/` and generate the missing files with the slug as title.

## Step 2: Read All Persistence Files

Read each file that exists:

- `docs/plans/{SLUG}-task_plan.md` — tasks, batches, dependencies
- `docs/plans/{SLUG}-findings.md` — patterns, open questions, research notes
- `docs/plans/{SLUG}-progress.md` — task statuses, batch log

## Step 3: Answer the 5-Question Reboot Test

Construct answers from persistence files: (1) Where am I — current batch/task from progress.md, (2) Where am I going — next task from task_plan.md, (3) What is the goal — title/design doc from task_plan.md, (4) What have I learned — findings/open questions from findings.md, (5) What have I done — completed tasks from progress.md.

See references/reboot-test.md for data sources, report format, and question details.

## Step 4: Re-read Relevant Source Files

From current/next task in task_plan.md, identify listed files. Check existence and read existing files to rebuild working context.

## Step 5: Report and Offer Actions

Recommend next action based on progress (continue in-progress task, start next batch, or review/handoff). Offer: continue execution, review plan, or update findings.

See references/reboot-test.md for action offer format.

## Rules

- Always answer all 5 reboot questions, even if some have minimal data
- Never modify task_plan.md during resume — it is read-only here
- Progress.md may be updated to reflect the recovery timestamp
- If the design doc is referenced and accessible, read it for goal context
- Report exact file paths so the user can navigate directly

---
name: resuming
description: Session recovery via 5-Question Reboot Test — read persistence files, rebuild context, report next action
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

Construct answers from the persistence files:

### 1. Where am I?

From progress.md: identify the current batch and current task (first non-done task in the active batch).

### 2. Where am I going?

From task_plan.md: identify the next incomplete task after the current one, following batch order.

### 3. What is the goal?

From task_plan.md header: extract the project title and design doc reference. Read the design doc if referenced and accessible.

### 4. What have I learned?

From findings.md: summarize key patterns found and resolved questions. Highlight any open questions that may affect the next task.

### 5. What have I done?

From progress.md: list all tasks with status "done" and their notes. Count completed vs total tasks.

Present the reboot test results:

```text
## 5-Question Reboot Test

1. WHERE AM I?
   Batch {N}, Task {ID}: {description}
   Status: {status}

2. WHERE AM I GOING?
   Next: Task {ID}: {description}
   Batch {N} has {X} remaining tasks

3. WHAT IS THE GOAL?
   {project title} -- {1-sentence summary from design doc}

4. WHAT HAVE I LEARNED?
   - {key finding 1}
   - {key finding 2}
   - Open: {unresolved question}

5. WHAT HAVE I DONE?
   {completed}/{total} tasks complete
   - {done task 1}
   - {done task 2}
```

## Step 4: Re-read Relevant Source Files

From the current/next task in task_plan.md, identify the files listed. Read each one to rebuild working context:

```bash
test -f {FILE_PATH} && echo "exists" || echo "not yet created"
```

Read existing files referenced by the current and next task.

## Step 5: Report and Offer Actions

Summarize the recovered state and recommend the next action based on progress:

- If current task is in-progress: recommend continuing it
- If current batch is complete: recommend starting next batch
- If all tasks are done: recommend review and handoff

```yaml
AskUserQuestion:
  question: "Session recovered. What would you like to do?"
  header: "Next Action"
  options:
    - label: "Continue execution"
      description: "Pick up from {CURRENT_TASK}"
    - label: "Review plan"
      description: "Display the full task plan for review"
    - label: "Update findings"
      description: "Add new findings or resolve open questions"
```

- "Continue execution" — report the current task details (files, acceptance criteria, TDD steps) and let the user proceed
- "Review plan" — display the full contents of task_plan.md
- "Update findings" — open findings.md and ask what to add or resolve

## Rules

- Always answer all 5 reboot questions, even if some have minimal data
- Never modify task_plan.md during resume — it is read-only here
- Progress.md may be updated to reflect the recovery timestamp
- If the design doc is referenced and accessible, read it for goal context
- Report exact file paths so the user can navigate directly

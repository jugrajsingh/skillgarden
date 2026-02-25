# 5-Question Reboot Test

## Questions and Data Sources

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

## Report Format

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

## Action Offer

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

- "Continue execution" — report the current task details (files, acceptance criteria, TDD steps)
- "Review plan" — display the full contents of task_plan.md
- "Update findings" — open findings.md and ask what to add or resolve

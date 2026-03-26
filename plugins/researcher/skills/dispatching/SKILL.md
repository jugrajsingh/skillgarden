---
name: dispatching
description: Use when you have 2+ independent problems that can be investigated in parallel by separate agents
allowed-tools:
  - Read
  - Glob
  - Grep
  - Task
  - AskUserQuestion
---

# Generic Parallel Dispatch

Validate problem independence with user, then delegate to the parallel-dispatcher agent for autonomous execution.

## Input

Problem list from $ARGUMENTS (newline or comma separated).

If $ARGUMENTS is empty, ask via AskUserQuestion:

```yaml
- question: "List the independent problems to investigate (one per line):"
  options:
    - "Enter problems separated by newlines"
    - "Enter problems separated by commas"
```

## Step 1: Parse and Validate Independence

Parse the problem list. For each pair, check for dependencies:

| Dependency Type | Detection | Action |
|----------------|-----------|--------|
| Shared state | Both reference same variable/config | Flag as dependent |
| Shared files | Both modify same file | Flag as dependent |
| Ordering | One problem's output is another's input | Flag as dependent |
| Conceptual | Related but no data dependency | Allow parallel |

If dependencies found, present them via AskUserQuestion:

```yaml
- question: "These problems have dependencies. How should I proceed?"
  options:
    - "Run sequentially in dependency order"
    - "Split into independent sub-problems"
    - "Proceed anyway (I accept potential conflicts)"
```

## Step 2: Cap and Group

Maximum 5 parallel agents. If more than 5 problems:

1. Group related problems by topic similarity
2. Present grouping via AskUserQuestion for approval

## Step 3: Dispatch Parallel Dispatcher Agent

Spawn the `parallel-dispatcher` agent via Task tool with:

- **problems**: The validated, independent problem list
- **project_path**: Current project root

The agent autonomously dispatches parallel sub-agents, collects results, detects conflicts, and merges findings.

## Step 4: Present Results

After the dispatcher completes, present the merged results.

If conflicts exist, ask user to resolve:

```yaml
- question: "Conflicts detected between agent findings. How to resolve?"
  options:
    - "I'll clarify — let me provide context"
    - "Accept both interpretations"
    - "Re-investigate the conflicting area"
```

## Output

```text
## Dispatch Complete

Problems: {total} dispatched, {successful} successful, {failed} failed
Conflicts: {count}

{merged results document}
```

## Rules

| Rule | Rationale |
|------|-----------|
| Max 5 parallel agents | Resource and context limits |
| Verify independence first | Dependent parallel tasks produce corrupt results |
| Never dispatch dependent problems in parallel | Ordering matters |
| Flag all conflicts | Silent resolution hides disagreements |
| Include failure reasons | Failed agents still provide useful signal |

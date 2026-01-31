---
name: dispatching
description: Generic parallel agent dispatch for independent problems — verify independence, dispatch, merge results
---

# Generic Parallel Dispatch

Dispatch parallel agents for a list of independent problems. Verify independence, dispatch via Task tool, merge results, and flag conflicts.

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

Parse the problem list. For each pair of problems, check for dependencies:

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
2. Present grouping via AskUserQuestion for approval:

```yaml
- question: "I grouped {N} problems into {M} groups. Approve grouping?"
  options:
    - "Approve grouping"
    - "Show me the groups first"
    - "Run first 5 only, queue the rest"
```

## Step 3: Dispatch Agents

For each problem, spawn a Task agent with:

- **Clear scope:** One problem, one output
- **Agent type** appropriate to the problem:

| Problem Type | Agent Approach |
|-------------|---------------|
| Codebase question | Use Glob, Grep, Read tools for exploration |
| Command/script task | Use Bash tool for execution |
| Mixed investigation | Use all available tools |

- **Output format:** Structured markdown with findings

Task prompt template:

```text
Investigate the following problem independently.

Problem: {problem statement}
Project root: {project path}

Produce structured findings in markdown:
## Problem: {problem statement}
### Findings
{detailed findings with file:line citations where applicable}
### Conclusion
{direct answer to the problem}
```

## Step 4: Collect Results

Wait for all Task agents to complete. Track status:

| Agent | Problem | Status |
|-------|---------|--------|
| 1 | {problem} | complete / failed / timeout |
| 2 | {problem} | complete / failed / timeout |

For failed agents, include the failure reason in the merged output.

## Step 5: Flag Conflicts

Compare results across agents. Flag conflicts when:

- Two agents report contradictory findings about the same code
- Two agents reach different conclusions about the same behavior
- File citations disagree on what code does

Present conflicts clearly:

```text
## Conflict Detected

Agent 1 (Problem: X) says: {finding}
Agent 2 (Problem: Y) says: {contradictory finding}

Both reference: path/to/file.py:42
```

## Step 6: Merge Results

Combine all agent outputs into a single document:

```text
## Dispatch Results

### Problem 1: {statement}
{agent output}

### Problem 2: {statement}
{agent output}

### Conflicts (if any)
{conflict details}
```

## Step 7: Present and Resolve

Present merged results. If conflicts exist, ask user to resolve:

```yaml
- question: "Conflicts detected between agents. How should I resolve?"
  options:
    - "Keep Agent 1's finding"
    - "Keep Agent 2's finding"
    - "Investigate further"
    - "Keep both with caveat"
```

## Rules

| Rule | Rationale |
|------|-----------|
| Max 5 parallel agents | Resource and context limits |
| Verify independence first | Dependent parallel tasks produce corrupt results |
| Never dispatch dependent problems in parallel | Ordering matters for dependent work |
| Each agent gets fresh context | No shared state between agents |
| Flag all conflicts | Silent resolution hides important disagreements |
| Include failure reasons | Failed agents still provide useful signal |

## Output

Present the final merged result:

```text
## Dispatch Complete

Problems: {total} dispatched, {successful} successful, {failed} failed
Conflicts: {count}

{merged results document}
```

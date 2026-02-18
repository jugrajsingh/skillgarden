---
name: dispatching
description: Use when you have 2+ independent problems that can be investigated in parallel by separate agents
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Task
  - AskUserQuestion
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

## Steps 5-7: Conflict Detection, Merge, and Resolution

Compare results across agents, flag contradictions, merge into single document, and ask user to resolve conflicts.

Full procedures and templates: `references/conflict-and-merge.md`

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

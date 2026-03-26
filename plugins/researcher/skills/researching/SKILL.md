---
name: researching
description: Use when you need to deeply investigate a codebase question using parallel sub-agents with persistent report output
allowed-tools:
  - Read
  - Glob
  - Grep
  - Task
  - Bash(mkdir *)
  - AskUserQuestion
---

# Parallel Research Workflow

Gather the research question from the user, then delegate to the research-orchestrator agent for autonomous parallel investigation.

## Input

Research question from $ARGUMENTS.

If $ARGUMENTS is empty, ask via AskUserQuestion:

```yaml
- question: "What would you like to research?"
  options:
    - "How does X work?"
    - "Where is X implemented?"
    - "What patterns does X use?"
    - "Compare approaches for X"
```

## Step 1: Generate Slug

Create a URL-safe slug from the research question (lowercase, hyphens, max 50 chars, strip articles).

```bash
mkdir -p docs/research
```

## Step 2: Dispatch Research Orchestrator

Spawn the `research-orchestrator` agent via Task tool with:

- **question**: The research question
- **slug**: Generated slug
- **project_path**: Current project root

The agent autonomously decomposes the question, dispatches parallel specialist agents (locator, analyzer, pattern-finder), reconciles results, and writes the report to `docs/research/{slug}-report.md`.

## Step 3: Present Results

After the orchestrator completes, read and present the report summary.

Offer next steps via AskUserQuestion:

```yaml
- question: "Research complete. What next?"
  options:
    - label: "Deep dive"
      description: "Investigate a specific finding further"
    - label: "Create plan"
      description: "Use findings to create an implementation plan"
    - label: "Done"
      description: "Research is sufficient"
```

- "Deep dive" — re-run with a narrowed sub-question
- "Create plan" — load the `planner:planning` skill, passing the report path
- "Done" — report the report path and exit

## Rules

| Rule | Rationale |
|------|-----------|
| file:line references mandatory | Every technical claim must be verifiable |
| Synonym expansion for searches | Single terms miss aliased concepts |
| Progressive disclosure | Overview first, details on demand |
| Max 5 parallel agents | Resource and context limits |
| No fabricated paths | If not found, report that clearly |

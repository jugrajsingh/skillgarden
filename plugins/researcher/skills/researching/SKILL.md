---
name: researching
description: Use when you need to deeply investigate a codebase question using parallel sub-agents with persistent report output
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Task
  - AskUserQuestion
---

# Parallel Research Workflow

Decompose a research question into sub-questions, dispatch parallel agents, and synthesize findings into a persistent report with file:line citations.

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

## Step 1: Decompose Question

Break the research question into 2-4 sub-questions. Each sub-question maps to an agent type based on its nature:

| Question Type | Agent | Model | Purpose |
|---------------|-------|-------|---------|
| WHERE is X? | locator | haiku | Find file paths grouped by purpose |
| HOW does X work? | analyzer | sonnet | Trace data flow, describe patterns |
| WHY is X designed this way? | analyzer | sonnet | Architectural decisions, trade-offs |
| WHAT PATTERNS does X follow? | pattern-finder | sonnet | Find similar implementations, variations |

### Decomposition Rules

- Minimum 2 sub-questions, maximum 4
- Each sub-question must be answerable independently
- Always include at least one WHERE question (locator) to ground the research
- Phrase sub-questions to be specific and scoped

## Step 2: Generate Slug

Create a URL-safe slug from the research question (lowercase, hyphens, max 50 chars, strip articles).

## Step 3: Dispatch Parallel Agents

Dispatch agents using the Task tool. Maximum 5 parallel agents.

For each sub-question, spawn a Task with:

1. **Agent context** from the corresponding agent file in this plugin's agents/ directory
2. **Sub-question** as the primary prompt
3. **Project path** for codebase access
4. **Output format** requirements per agent type

For each agent type (locator, analyzer, pattern-finder), use the prompt templates in `references/agent-prompts.md`.

## Step 4: 2-Action Rule

After every 2 search/read operations within any agent, save intermediate findings.

- If `docs/plans/{slug}-findings.md` exists, append findings there
- Otherwise, keep intermediate state in agent context
- This prevents loss of progress on long research tasks

## Step 5: Collect and Reconcile Results

Gather outputs from all completed agents. Check for conflicts:

| Conflict Type | Resolution |
|---------------|------------|
| Different files cited for same function | Verify which is current via git log |
| Contradictory behavior descriptions | Re-read the disputed file, report both interpretations |
| Missing coverage | Note in Gaps section |

Flag any conflicts explicitly in the report. Do not silently resolve them.

## Step 6: Write Research Report

Write to `docs/research/{slug}-report.md`. Full report structure, frontmatter, section templates, and output summary: `references/report-format.md`

## Step 7: Update Planning Files

If `docs/plans/{slug}-findings.md` exists, append key findings with file:line references and date stamp.

## Rules

| Rule | Rationale |
|------|-----------|
| file:line references mandatory | Every technical claim must be verifiable |
| Synonym expansion for searches | Single terms miss aliased concepts |
| Progressive disclosure | Overview first, details on demand |
| Max 5 parallel agents | Resource and context limits |
| 2-Action Rule | Prevent progress loss on long research |
| No fabricated paths | If not found, report that clearly |

## Synonym Expansion

Always expand search terms: config→settings/options/conf, error→exception/failure, handler→processor/callback, auth→login/session/token. Full table in `references/agent-prompts.md`.

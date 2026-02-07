---
name: researching
description: Parallel sub-agent research with persistent reports — decompose questions, dispatch agents, synthesize findings
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

### Example Decomposition

Question: "How does authentication work in this project?"

| # | Sub-question | Agent |
|---|-------------|-------|
| 1 | Where are the authentication files? | locator |
| 2 | How does the login flow process requests? | analyzer |
| 3 | What patterns do the auth middleware follow? | pattern-finder |

## Step 2: Generate Slug

Create a URL-safe slug from the research question:

- Lowercase, hyphens for spaces
- Strip articles (a, an, the)
- Max 50 characters
- Example: "How does authentication work?" becomes `how-does-authentication-work`

## Step 3: Dispatch Parallel Agents

Dispatch agents using the Task tool. Maximum 5 parallel agents.

For each sub-question, spawn a Task with:

1. **Agent context** from the corresponding agent file in this plugin's agents/ directory
2. **Sub-question** as the primary prompt
3. **Project path** for codebase access
4. **Output format** requirements per agent type

### Locator Agent Task

Prompt the Task with:

```text
You are a locator agent. Find WHERE the following exists in the codebase.

Sub-question: {sub-question}
Project root: {project path}

Search using Glob for file patterns and Grep for content.
Use synonym expansion — search multiple term variations:
  "config" also search "settings", "options", "preferences", "conf"
  "error" also search "exception", "failure", "fault"
  "handler" also search "processor", "listener", "callback"
  "auth" also search "login", "session", "token", "credential"

Output format — group files by purpose:
## Files Found
### Implementation
- path/to/file.py — {brief description}
### Tests
- tests/test_file.py — {brief description}
### Configuration
- config/settings.yaml — {brief description}
### Types/Interfaces
- types/models.py — {brief description}
### Documentation
- docs/feature.md — {brief description}
```

### Analyzer Agent Task

Prompt the Task with:

```text
You are an analyzer agent. Understand HOW the following works.

Sub-question: {sub-question}
Project root: {project path}
Known files: {locator output if available, otherwise "discover via search"}

Read relevant files. Trace data flow. Document with file:line references.
Every technical claim MUST include a file:line citation.
If uncertain, mark with triangle (caveat indicator).

Output format:
## Analysis: {sub-question}
### Summary
{2-3 sentence answer}
### Data Flow
1. Entry point: path/file.py:42 — {description}
2. Processing: path/other.py:15 — {description}
3. Output: path/result.py:88 — {description}
### Patterns Observed
- {pattern name}: file.py:10-25 — {how it works}
### Architectural Notes
- {observation with file:line citation}
```

### Pattern-Finder Agent Task

Prompt the Task with:

```text
You are a pattern-finder agent. Find existing code patterns to model after.

Sub-question: {sub-question}
Project root: {project path}
Known files: {locator output if available, otherwise "discover via search"}

Find multiple instances of the same pattern. Show each variation with context.
Use synonym expansion for search terms.
Max 20 lines per code snippet.

Output format:
## Patterns: {what was searched}
### Variation 1: {location}
File: path/to/file.py:15-30
{code snippet}
Context: {why this instance is relevant}
### Variation 2: {location}
File: path/to/other.py:42-55
{code snippet}
Context: {how this differs from variation 1}
### Recommendation
{which variation to follow and why}
```

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

Read the template at `${CLAUDE_PLUGIN_ROOT}/templates/research-report.md`.

Write the report to `docs/research/{slug}-report.md` with this structure:

### YAML Frontmatter

```yaml
---
question: {original research question}
date: {YYYY-MM-DD}
agents: [locator, analyzer, pattern-finder]
status: complete | partial | inconclusive
---
```

Status meanings:

| Status | Meaning |
|--------|---------|
| complete | All sub-questions answered with citations |
| partial | Some sub-questions unanswered or missing citations |
| inconclusive | Conflicting findings or insufficient evidence |

### _OVERVIEW Section

2-3 sentence direct answer to the original question. No hedging. If uncertain, state what IS known and what IS NOT.

### Detail Sections

One section per sub-question. Each section must include:

- Section header matching the sub-question
- Findings with file:line citations
- Code snippets where relevant (max 20 lines each)
- Agent attribution (which agent produced this finding)

### Cross-References

Link related findings across sections. Example:

```text
The auth middleware (see Section 2) uses the token format defined in Section 3.
```

### Gaps Section

What could not be determined and why. Include:

- Unanswered aspects of the original question
- Files that could not be located
- Suggested next steps for further investigation

## Step 7: Update Planning Files

If `docs/plans/{slug}-findings.md` exists:

- Append key findings from the report
- Include file:line references
- Add date stamp for the research

## Rules

| Rule | Rationale |
|------|-----------|
| file:line references mandatory | Every technical claim must be verifiable |
| Synonym expansion for searches | Single terms miss aliased concepts |
| Progressive disclosure | Overview first, details on demand |
| Max 5 parallel agents | Resource and context limits |
| 2-Action Rule | Prevent progress loss on long research |
| No fabricated paths | If not found, report that clearly |

## Synonym Expansion Reference

| Primary Term | Also Search |
|-------------|-------------|
| config | settings, options, preferences, conf, configuration |
| error | exception, failure, fault, err |
| handler | processor, listener, callback, hook |
| auth | login, session, token, credential, authentication |
| test | spec, check, verify, assertion |
| model | schema, entity, record, type |
| route | endpoint, path, url, api |
| store | repository, dao, persistence, database, db |
| validate | check, verify, sanitize, parse |
| transform | convert, map, serialize, deserialize |

## Output

Present the completed report path and a brief summary:

```text
## Research Complete

Report: docs/research/{slug}-report.md
Status: {status}
Agents: {count} dispatched, {count} successful

### Key Findings
- {finding 1 with file:line}
- {finding 2 with file:line}
- {finding 3 with file:line}

### Gaps
- {gap 1}
```

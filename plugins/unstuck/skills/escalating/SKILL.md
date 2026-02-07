---
name: escalating
description: Strike 3 — broader rethink, external search, and structured user escalation
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - WebSearch
  - AskUserQuestion
---

# Escalating

Strike 3 of the unstuck protocol. Two targeted attempts failed — broaden the search and involve the user.

## Step 1: Question Fundamental Assumptions

Two strikes failed. Something foundational may be wrong:

- Is the overall pattern/architecture sound for this use case?
- Is this the right tool/library/framework for the job?
- Could this be an upstream bug (dependency, platform, infrastructure)?
- Is the requirement itself contradictory or impossible?
- Are we solving the right problem? (maybe the error is a symptom, not the cause)

## Step 2: Search for External Solutions

Search for the exact error message and relevant context:

```text
WebSearch: "{EXACT_ERROR_MESSAGE} {FRAMEWORK} {LANGUAGE}"
```

Check:

- GitHub Issues on the relevant library — is this a known bug?
- Stack Overflow — has someone solved this exact problem?
- Official documentation — are we using the API correctly?
- Release notes — did a recent version introduce breaking changes?

## Step 3: Knowledge Pack Patterns

If a knowledge pack was loaded:

- Review "Known Patterns" section for recurring resolutions
- Check if the issue maps to an architectural pattern, not just a code bug

## Step 4: Synthesize Findings

Compile everything learned across all three strikes:

```text
What we know:
- Strike 1 ruled out: {LIST}
- Strike 2 ruled out: {LIST}
- External search found: {FINDINGS}
- Remaining hypotheses: {LIST}
```

## Step 5: Escalate to User

Present a structured escalation:

```yaml
AskUserQuestion:
  question: "I've hit a wall after 3 investigation attempts. Here's what I found — can you provide guidance?"
  header: "Escalation"
  options:
    - label: "Share context"
      description: "I have additional context that might help (env details, recent changes, known issues)"
    - label: "Try hypothesis"
      description: "Pick from the remaining hypotheses and test it"
    - label: "Different direction"
      description: "Abandon this approach entirely, suggest an alternative"
    - label: "Accept workaround"
      description: "Use a temporary workaround while the root cause is investigated later"
```

Before asking, output the full context:

```text
## Escalation Report

### Problem
{PROBLEM_SUMMARY}

### What Was Tried
Strike 1 (Diagnose): {APPROACH} → {OUTCOME}
Strike 2 (Pivot):    {APPROACH} → {OUTCOME}

### Errors Encountered
{SPECIFIC_ERRORS}

### Remaining Hypotheses
{NUMBERED_LIST}

### External References
{URLS_OR_FINDINGS}
```

## Step 6: Act on User Guidance

Based on user response:

- **Share context**: Incorporate new info, retry most promising hypothesis
- **Try hypothesis**: Execute the selected hypothesis with same rigor as Strike 1
- **Different direction**: Abandon current approach, implement user's alternative
- **Accept workaround**: Implement minimal workaround, document tech debt in RCA

## Outcome

Report to the orchestrator:

```text
Escalation:
  User guidance: {SUMMARY}
  Action taken: {WHAT_WAS_DONE}
  Result: { resolved | workaround | deferred }
  Notes: {ADDITIONAL_CONTEXT}
```

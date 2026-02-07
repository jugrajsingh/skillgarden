---
name: diagnosing
description: Strike 1 — root cause investigation with evidence gathering and hypothesis testing
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
---

# Diagnosing

Strike 1 of the unstuck protocol. Systematic root cause investigation.

## Pre-Check: Knowledge Pack

If a knowledge pack was loaded by the orchestrator:

1. Scan the "Common Errors" table — does the error match a known pattern?
2. If match found: follow the "Check" column directly before generic investigation
3. Run relevant "Diagnostic Commands" from the knowledge pack
4. Check "Gotchas" for framework-specific traps

If a match resolves the issue, report resolved and skip remaining steps.

## Step 1: Read the Error Completely

- Read the FULL stack trace, not just the last line
- Note the originating file and line number
- Identify the error type/code (e.g., `TypeError`, HTTP 422, exit code 1)
- Check if the error message contains a suggestion or hint

```text
Record:
- Error type: {TYPE}
- Error message: {MESSAGE}
- Origin: {FILE}:{LINE}
- Error code: {CODE} (if any)
```

## Step 2: Reproduce Consistently

- Identify the exact command or action that triggers the error
- Run it once to confirm it still fails
- Note if it fails consistently or intermittently

If intermittent: gather 3 runs, note which succeed/fail and any differences.

## Step 3: Check Recent Changes

```bash
git diff HEAD~3 --stat
git log --oneline -5
```

- Did a recent change touch the failing file or its dependencies?
- Were config files, dependencies, or environment changed recently?
- Was a library updated that could cause breaking changes?

## Step 4: Gather Evidence at Boundaries

Trace the data flow backward from the error:

1. Read the failing function/method
2. Check the inputs to that function — are they what you expect?
3. Check the caller — is it passing correct arguments?
4. Check configuration/environment values used in the flow

At each boundary, verify: "Is the data correct here?"

Find the boundary where data goes from correct → incorrect. That boundary contains the bug.

## Step 5: Form a Single Hypothesis

Based on evidence gathered:

```text
Hypothesis: "{X} is the cause because {Y}"
Evidence supporting: {LIST}
Evidence against: {LIST}
```

The hypothesis must be specific and testable — not "something is wrong with auth" but "the JWT token is missing the `sub` claim because the user ID is None at token creation."

## Step 6: Test Minimally

- Make the smallest possible change to test the hypothesis
- Change ONE variable at a time
- If the fix works: verify it doesn't break anything else
- If the fix doesn't work: the hypothesis was wrong — record what was learned

## Outcome

Report to the orchestrator:

```text
Diagnosis:
  Hypothesis: {HYPOTHESIS}
  Change made: {DESCRIPTION}
  Result: { resolved | not resolved }
  Evidence: {WHAT_WAS_LEARNED}
```

If resolved, include what fixed it and why.
If not resolved, include why the hypothesis was wrong and what was ruled out.

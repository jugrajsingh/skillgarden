---
name: getting-unstuck
description: Structured error escalation protocol — 3-strike workflow to diagnose, pivot, and escalate when stuck
---

# Getting Unstuck

Structured escalation when stuck on a problem. Three strikes: diagnose → pivot → escalate.

## Input

`$ARGUMENTS` = description of the issue (error message, failing behavior, what was tried).

If `$ARGUMENTS` is empty, ask:

```yaml
AskUserQuestion:
  question: "What are you stuck on? Describe the error, failing behavior, or what you've tried."
  header: "Problem"
  options:
    - label: "Build/compile error"
      description: "Code won't build, type errors, import failures"
    - label: "Runtime error"
      description: "Crashes, exceptions, unexpected behavior at runtime"
    - label: "Test failure"
      description: "Tests failing, assertions wrong, flaky tests"
    - label: "Behavior mismatch"
      description: "Code runs but produces wrong results"
```

## Step 1: Capture the Problem

Gather:

- Exact error message or failing behavior from `$ARGUMENTS`
- Stack trace if available (read from terminal output or logs)
- What was already tried before invoking /unstuck
- Which file(s) are involved

Summarize the problem in 2-3 sentences. This becomes the RCA Problem section.

## Step 2: Detect Context

Identify language and framework from:

1. Error message patterns (e.g., `pydantic`, `FastAPI`, `asyncio` in traceback)
2. File extensions of involved files
3. Project manifest files (`pyproject.toml`, `package.json`, `go.mod`, `Cargo.toml`)

Store detected context: `{LANGUAGE}` and `{FRAMEWORK}` (may be empty).

## Step 3: Load Knowledge Pack

If `{LANGUAGE}` and `{FRAMEWORK}` are identified:

```bash
test -f "${CLAUDE_PLUGIN_ROOT}/knowledge/{LANGUAGE}-{FRAMEWORK}.md" && echo "found"
```

If found, read `${CLAUDE_PLUGIN_ROOT}/knowledge/{LANGUAGE}-{FRAMEWORK}.md`.

Hold the knowledge pack in context — skills reference it during investigation.

## Step 4: Initialize RCA File

Generate slug from the problem summary (lowercase, hyphenated, max 5 words).

```bash
mkdir -p docs/rcas
```

Read `${CLAUDE_PLUGIN_ROOT}/templates/rca.md` and create `docs/rcas/{YYYY-MM-DD}-{SLUG}.md`:

- Replace `{TITLE}` with the problem summary
- Replace `{DATE}` with today's date
- Fill the Problem section from Step 1
- Fill Error Evidence with the exact error/stack trace

Track the RCA path as `{RCA_FILE}` for updates throughout.

## Step 5: Strike 1 — Diagnose

Load the `unstuck:diagnosing` skill and follow it.

Pass context:

- Problem summary from Step 1
- Knowledge pack contents (if loaded)
- RCA file path `{RCA_FILE}`

After diagnosing returns:

- Update `{RCA_FILE}` Investigation Log — Strike 1 row with approach and result
- If the skill reports **resolved**: update RCA Status to `resolved`, fill Resolution and Lessons Learned, done

If not resolved, proceed to Strike 2.

## Step 6: Strike 2 — Pivot

Load the `unstuck:pivoting` skill and follow it.

Pass context:

- Problem summary
- What Strike 1 tried and why it failed
- Knowledge pack contents (if loaded)
- RCA file path `{RCA_FILE}`

After pivoting returns:

- Update `{RCA_FILE}` Investigation Log — Strike 2 row
- If **resolved**: update RCA Status to `resolved`, fill Resolution and Lessons Learned, done

If not resolved, proceed to Strike 3.

## Step 7: Strike 3 — Escalate

Load the `unstuck:escalating` skill and follow it.

Pass context:

- Problem summary
- Strike 1 and 2 attempts and failures
- Knowledge pack contents (if loaded)
- RCA file path `{RCA_FILE}`

After escalating returns:

- Update `{RCA_FILE}` Investigation Log — Strike 3 row
- Update RCA Status to `escalated` or `resolved` based on outcome
- Fill Resolution with user guidance received (if any)

## Completion

Report:

```text
## Unstuck Summary

Status: { resolved | escalated }
RCA:    {RCA_FILE}
Strikes: {N}/3

Strike 1 (Diagnose): { one-line outcome }
Strike 2 (Pivot):    { one-line outcome }
Strike 3 (Escalate): { one-line outcome }
```

## Rules

- NEVER repeat the exact same failing action between strikes
- Each strike must try something fundamentally different
- Always update the RCA file after each strike
- If resolved at any strike, stop — do not continue to the next
- Keep the RCA file as a persistent artifact for future reference

---
name: verifying
description: Use when about to claim work is complete — runs test suite, checks acceptance criteria, and collects concrete evidence
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
  - AskUserQuestion
---

# Verification Gate

Run evidence-based verification: test suite execution, acceptance criteria checking, regression detection, and gate decision.

## Input

$ARGUMENTS = optional scope (slug or "current plan").

If $ARGUMENTS is empty:

- Check current branch name for a slug (e.g., feature/add-auth -> add-auth)
- Check docs/plans/ for a matching task_plan.md
- If no plan found, verify based on test suite and commit history only

## Step 1: Run Full Test Suite

Detect the test runner from project files:

- pyproject.toml or pytest.ini or setup.cfg -> pytest
- package.json with test script -> npm test
- Cargo.toml -> cargo test
- go.mod -> go test ./...
- If multiple, prefer the primary language of the project

Execute the test suite and capture full output (stdout + stderr):

```bash
# Example for Python:
pytest --tb=short -v 2>&1
```

Record results:

- Total tests run
- Passed count
- Failed count
- Skipped count
- Execution time
- Any warnings produced

If the test suite fails to run at all (import errors, configuration issues), report this as a critical failure immediately.

## Step 2: Load Acceptance Criteria

Source acceptance criteria based on available context:

**If slug provided and plan exists:**

- Read docs/plans/{slug}/task_plan.md
- Extract acceptance criteria from each task definition
- Also extract the plan-level success criteria if present

**If no plan available:**

- Extract criteria from commit messages:

  ```bash
  git log develop...HEAD --format="%B" | grep -i "acceptance\|criteria\|verify"
  ```

- Extract from PR description if one exists
- If no criteria found, report: "No acceptance criteria found. Verification limited to test suite results."

List each criterion with a number for reference.

## Steps 3-5: Evidence Collection, Regression Check, Report

For each criterion, collect concrete evidence (test output, file diff, command output). Run regression check on broader suite. Generate verification report.

Full procedures, evidence rules, and report template: `references/evidence-collection.md`

## Gate Decision Logic

The gate is PASS only when ALL of the following are true:

- Test suite passes (zero failures)
- ALL acceptance criteria are VERIFIED
- Regression check shows no failures

The gate is BLOCKED when ANY of the following are true:

- Test suite has failures
- Any acceptance criterion is FAILED
- Regression check reveals failures

If BLOCKED, list every failure explicitly:

```text
### Gate Decision
BLOCKED

Failures:
1. Test suite: {N} tests failing
2. Criterion #2: {what failed}
3. Regression: {what regressed}

Recommended actions:
1. {specific action to fix failure 1}
2. {specific action to fix failure 2}
```

## Rules

- Evidence before claims — never assert something is working without proof
- Run actual commands — do not rely on memory or assumptions about test state
- Forbidden in verification language: "should", "probably", "seems to", "likely", "I think", "appears to"
- Every VERIFIED criterion has concrete evidence attached
- Gate is binary: PASS or BLOCKED, no partial pass
- If test runner cannot be detected, ask user via AskUserQuestion for the test command

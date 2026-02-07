---
name: verifying
description: Evidence-before-claims verification gate — test suite, acceptance criteria, regression check, evidence collection
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

## Step 3: Verify Each Criterion

For EACH acceptance criterion, collect concrete evidence:

**Types of evidence:**

1. Test output — grep test results for tests that exercise this criterion

   ```bash
   pytest -v -k "{related_test_name}" 2>&1
   ```

2. File diff — show the implementation that satisfies the criterion

   ```bash
   git diff develop...HEAD -- {relevant_file}
   ```

3. Command output — run a command that demonstrates the result

   ```bash
   # e.g., python -c "from module import feature; print(feature())"
   ```

**For each criterion, record:**

- Criterion number and text
- Status: VERIFIED or FAILED
- Evidence: exact output or file reference that proves the status
- If FAILED: what specifically is wrong, with file:line if applicable

**Evidence rules:**

- Every VERIFIED claim must have concrete evidence attached
- Forbidden words in verification claims: "should", "probably", "seems to", "likely", "I think", "appears to"
- Use definitive language: "Test X passes with output Y", "File Z contains implementation at line N"
- If evidence is ambiguous, mark as FAILED with explanation

## Step 4: Regression Check

Run the broader test suite (not just tests related to new changes):

```bash
# Full suite
pytest --tb=short 2>&1
```

Check for:

1. **New warnings** — compare test output for warning messages that weren't present before
2. **Performance degradation** — if test execution time is available from CI or previous runs, check for >2x increase
3. **Flaky tests** — if any test failed, run it again to check for flakiness:

   ```bash
   pytest {failed_test} -v --count=2 2>&1
   ```

   (If pytest-repeat is not available, run the test twice manually)

Record regression check results:

- Broader suite pass/fail
- New warning count
- Performance assessment: normal or degraded
- Flaky test count

## Step 5: Generate Verification Report

```text
## Verification Report

### Test Suite
- Runner: {runner_name}
- Status: {PASS or FAIL}
- Tests: {passed}/{total} ({skipped} skipped)
- Duration: {time}
- Warnings: {count}

### Acceptance Criteria
| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | {criterion text} | VERIFIED | {concrete evidence reference} |
| 2 | {criterion text} | FAILED | {what is wrong} |

### Regression Check
- Broader suite: {PASS or FAIL}
- New warnings: {count}
- Performance: {normal or degraded}
- Flaky tests: {count}

### Gate Decision
{PASS or BLOCKED}
```

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

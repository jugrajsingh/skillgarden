# Evidence Collection and Verification

## Verify Each Criterion

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

## Regression Check

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

## Verification Report Template

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

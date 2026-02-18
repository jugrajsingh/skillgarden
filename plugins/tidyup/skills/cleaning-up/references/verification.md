# Phase 6: Verify

## Run Test Suite

Detect the test runner from project configuration:

| File | Runner | Command |
|------|--------|---------|
| pytest.ini / pyproject.toml (pytest) | pytest | `pytest` |
| package.json | npm/yarn | `npm test` |
| Cargo.toml | cargo | `cargo test` |
| go.mod | go | `go test ./...` |
| Makefile (test target) | make | `make test` |

Run the detected test suite:

```bash
{TEST_COMMAND}
```

## Handle Test Failures

If tests fail after a change:

1. Identify which cleanup action caused the failure
2. Revert that specific change (re-read file from git):

   ```bash
   git checkout -- {FILE}
   ```

3. Report the failure to user with details
4. Continue with remaining cleanup items

## Generate Cleanup Report

Use the template from `templates/cleanup-report.md` as the structure.

Fill in all sections:

```text
## Cleanup Report: {SCOPE}

### Actions Taken
| Action | File | Type | Details |
|--------|------|------|---------|
| Removed | path:line | dead code | {description} |
| Consolidated | pathA + pathB | duplication | {description} |
| Archived | path -> .archive/path | stale | {description} |

### Metrics
- Lines removed: {N}
- Files archived: {N}
- Duplicates consolidated: {N}

### Test Results
- Suite: {runner}
- Status: {pass/fail}
- Tests: {passed}/{total}

### Verification
- All references intact
- Tests passing
- No information lost (archived, not deleted)
```

If any verification item fails, mark it and explain.

---
name: tdd-cycling
description: RED-GREEN-REFACTOR cycle enforcement — write failing test, minimal code, refactor with safety net
---

# TDD Cycle

Execute a single RED-GREEN-REFACTOR cycle for a task.

## Input

$ARGUMENTS = task description with test name and assertion.

If $ARGUMENTS is missing test details, ask via AskUserQuestion for:

1. Test name — suggest format: test_should_{behavior}_when_{condition}
2. What to assert — the expected outcome or behavior

## Step 1: Determine Test Location

1. Check for existing test directories in the project root:
   - tests/ (Python pytest convention)
   - test/ (generic)
   - __tests__/ (JavaScript convention)
   - spec/ (Ruby/JS convention)
2. If multiple exist, use the one matching the implementation language
3. If none exist, create tests/ directory
4. Mirror the source file path in the test directory (e.g., src/utils/parser.py -> tests/utils/test_parser.py)

## RED Phase

__Goal: Write a failing test that defines the desired behavior.__

1. Write the test:
   - Test name follows: test_should_{behavior}_when_{condition}
   - Single assertion per test (or closely related assertions)
   - Clear arrange-act-assert structure
   - Use descriptive variable names in the test

2. Run the test:

   ```bash
   # Detect runner and execute
   # Python: pytest {test_file}::{test_name} -v
   # JavaScript: npx jest {test_file} -t "{test_name}"
   # Go: go test -run {test_name} ./...
   ```

3. Verify the failure:
   - Test MUST fail
   - Failure must be for the RIGHT reason:
     - CORRECT failures: ImportError (module doesn't exist), AttributeError (function doesn't exist), AssertionError (wrong return value)
     - WRONG failures: SyntaxError in the test, wrong import path, test framework misconfiguration
   - If test fails for the wrong reason: fix the test infrastructure and re-run
   - If test passes unexpectedly: the feature may already exist. Investigate, report findings, and ask user via AskUserQuestion whether to proceed with a different test or stop

4. Record RED state:
   - Test name and file path
   - Failure message (exact output)
   - Confirmation that failure is for the right reason

## GREEN Phase

__Goal: Write the MINIMAL code to make the test pass.__

1. Write implementation:
   - Only what the test requires — nothing more
   - No extra methods, no additional error handling beyond what's tested
   - No premature optimization
   - Hardcoded values are acceptable if that's all the test needs (they'll be generalized when more tests are added)

2. Run the test:

   ```bash
   # Same command as RED phase
   ```

3. Verify the pass:
   - Test MUST pass
   - If still failing, iterate on the implementation:
     - Attempt 1: re-read test, fix logic error
     - Attempt 2: check types and edge cases
     - Attempt 3: reconsider approach
     - After 3 attempts: flag for user via AskUserQuestion with details of what's failing and why

4. Run broader test suite:

   ```bash
   # Python: pytest --tb=short
   # JavaScript: npx jest
   # Go: go test ./...
   ```

   - Check for regressions — new code must not break existing tests
   - If regressions found: fix them while keeping the new test green

5. Record GREEN state:
   - Implementation file and line range
   - Test result: passed
   - Broader suite result: {passed}/{total}

## REFACTOR Phase

__Goal: Improve code quality while keeping all tests green.__

1. Review the code written in GREEN phase. Look for:
   - Duplicated logic that can be extracted into helpers
   - Poor variable or function names
   - Overly complex expressions that can be simplified
   - Missing type annotations
   - Opportunities to apply project conventions

2. Apply improvements one at a time:
   - Make a single refactoring change
   - Run tests immediately after
   - If tests break: revert the change, try a different approach
   - Continue until code is clean

3. What NOT to do during REFACTOR:
   - Do NOT add new behavior or features
   - Do NOT add new test cases
   - Do NOT change what the code does, only how it does it
   - Do NOT optimize prematurely

4. Record REFACTOR state:
   - Description of each refactoring applied
   - Test results after refactoring: {passed}/{total}

## Commit

Stage files explicitly (never wildcards, never git add -A):

```bash
git add {test_file_path} {implementation_file_path}
```

Commit options:

- If test and implementation are tightly coupled (single feature):

  ```text
  feat(scope): add {feature_description}
  ```

- If they should be separate commits:

  ```text
  test(scope): add {test_name}
  ```

  then

  ```text
  feat(scope): implement {feature_description}
  ```

No AI footers. Conventional format only.

## Report

Present the cycle results:

```text
## TDD Cycle Complete

### RED
- Test: {test_name}
- File: {test_file}:{line_number}
- Failure: {expected failure message}

### GREEN
- Implementation: {impl_file}:{line_range}
- Tests: {passed}/{total}

### REFACTOR
- Changes: {description of refactoring applied}
- Tests: {passed}/{total} (still green)

### Commit
- {commit_hash} {commit_message}
```

## Rules

- NEVER write production code without a failing test first
- Test names follow test_should_{behavior}_when_{condition} format
- Minimal code in GREEN — no gold plating, no extra features
- REFACTOR must not change behavior — only structure and style
- Always run tests between phases — never assume green
- One logical change per TDD cycle
- Explicit file paths in git add — no wildcards
- No AI footers in commits

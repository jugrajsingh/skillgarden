---
name: tdd-cycling
description: Use when implementing a feature or fix that needs a single RED-GREEN-REFACTOR TDD cycle
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
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

## RED → GREEN → REFACTOR

Execute the three phases sequentially. Each phase has verification steps and recording requirements.

- __RED__: Write failing test, verify it fails for the right reason (ImportError/AttributeError/AssertionError — not SyntaxError)
- __GREEN__: Write minimal code to pass, run broader suite to check regressions
- __REFACTOR__: One change at a time, run tests after each, never add new behavior

Full step-by-step procedures, runner detection, and failure handling: `references/phase-details.md`

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

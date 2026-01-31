---
name: pivoting
description: Strike 2 — alternative approach when initial diagnosis failed
---

# Pivoting

Strike 2 of the unstuck protocol. The diagnosis fix didn't work — try a fundamentally different approach.

## Rule

NEVER repeat what Strike 1 already tried. The diagnosis failed — doing it again won't help.

## Pre-Check: Knowledge Pack

If a knowledge pack was loaded:

1. Check "Gotchas" — is this a known framework trap that wastes debugging time?
2. Check "Known Patterns" — has this been seen before with a known resolution?
3. If a gotcha or pattern matches, apply it directly

## Step 1: Find Working Examples

Search the codebase for similar code that works:

```bash
# Find similar patterns in the codebase
grep -rn "{RELEVANT_PATTERN}" --include="*.{EXT}" | head -20
```

- Find a working instance of the same operation (API call, DB query, auth flow, etc.)
- If no working example exists in the codebase, search project dependencies or docs

## Step 2: Compare Working vs Broken

List every difference between the working code and the broken code:

```text
| Aspect | Working | Broken |
|--------|---------|--------|
| ... | ... | ... |
```

Focus on: imports, configuration, argument order, types, async/sync mismatch, middleware/decorator order.

## Step 3: Challenge Assumptions

Question what Strike 1 took for granted:

- Is the environment actually configured correctly? (check env vars, config files)
- Is the dependency version compatible? (check lock file, not just manifest)
- Is the data actually in the expected format? (log raw values)
- Is the code actually being executed? (add a log/print at the entry point)

## Step 4: Try a Different Method

Pick ONE alternative approach:

| If Strike 1 tried... | Pivot to... |
|-----------------------|-------------|
| Fixing the current code | Using a different library/API |
| Debugging data flow | Rewriting the function from scratch |
| Config changes | Hardcoding values to isolate the issue |
| Async approach | Sync equivalent (or vice versa) |
| Complex solution | Simplest possible implementation |

Implement the alternative. Test with the same verification as Strike 1.

## Step 5: Verify

- Does the alternative approach pass the original test case?
- Does it break any existing functionality?
- Is it a viable long-term solution (not just a hack)?

## Outcome

Report to the orchestrator:

```text
Pivot:
  Approach: {WHAT_WAS_TRIED}
  Differs from Strike 1: {HOW}
  Result: { resolved | not resolved }
  Evidence: {WHAT_WAS_LEARNED}
```

If resolved, include the alternative that worked and why.
If not resolved, include what was ruled out — this narrows the search for Strike 3.

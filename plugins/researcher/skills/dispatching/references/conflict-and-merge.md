# Conflict Detection and Result Merging

## Flag Conflicts

Compare results across agents. Flag conflicts when:

- Two agents report contradictory findings about the same code
- Two agents reach different conclusions about the same behavior
- File citations disagree on what code does

Present conflicts clearly:

```text
## Conflict Detected

Agent 1 (Problem: X) says: {finding}
Agent 2 (Problem: Y) says: {contradictory finding}

Both reference: path/to/file.py:42
```

## Merge Results

Combine all agent outputs into a single document:

```text
## Dispatch Results

### Problem 1: {statement}
{agent output}

### Problem 2: {statement}
{agent output}

### Conflicts (if any)
{conflict details}
```

## Present and Resolve

Present merged results. If conflicts exist, ask user to resolve:

```yaml
- question: "Conflicts detected between agents. How should I resolve?"
  options:
    - "Keep Agent 1's finding"
    - "Keep Agent 2's finding"
    - "Investigate further"
    - "Keep both with caveat"
```

## Final Output

```text
## Dispatch Complete

Problems: {total} dispatched, {successful} successful, {failed} failed
Conflicts: {count}

{merged results document}
```

# Batch Execution Protocol

## Pipeline Per Task

```text
T01 → [Implement] → [Spec Review] → [Quality Review]
         ↓ fail         ↓ fail            ↓ findings
       retry (1x)    flag + stop      report + continue
```

Each stage is a separate subagent with its own context. No shared state between stages except the explicit handoff (report + file list).

## Native Task Dependencies

For task T01 in Batch 1:

- TaskCreate: "Implement T01" (no blockers)
- TaskCreate: "Spec-review T01" (blockedBy: implement T01)
- TaskCreate: "Quality-review T01" (blockedBy: spec-review T01)

For task T02 in the same batch:

- TaskCreate: "Implement T02" (no blockers — parallel with T01)
- TaskCreate: "Spec-review T02" (blockedBy: implement T02)
- TaskCreate: "Quality-review T02" (blockedBy: spec-review T02)

Tasks within the same batch can run in parallel. Cross-task dependencies only exist across batches (Batch 2 waits for Batch 1).

## Batch Checkpoint

After each batch completes:

1. All native Tasks in batch resolved (completed, blocked, or skipped)
2. progress.md updated with results for every task
3. User prompted: continue / pause / abort

## Failure Handling

| Stage | Failure | Action |
|-------|---------|--------|
| Implement | Tests fail | Retry once with adjusted approach, then flag |
| Implement | Cannot create files | Flag immediately, likely a path issue |
| Spec review | Deviations found | Stop pipeline for this task, flag for user |
| Spec review | Cannot read files | Flag immediately, likely implementation issue |
| Quality review | Critical finding | Flag, suggest fix before next batch |
| Quality review | Major finding | Report, continue (user can address later) |
| Quality review | Minor finding | Report, continue |

## Retry Protocol

Implementation retry (max 1):

1. Analyze why tests failed
2. Adjust approach (different algorithm, fix misunderstanding)
3. Re-run RED-GREEN-REFACTOR from scratch
4. If still failing, mark as blocked with detailed failure report

No retries for spec review or quality review — these are verification stages that report facts.

## Progress Sync

Native Task status maps to progress.md as follows:

- in_progress → in_progress (task is being worked on)
- completed → done (with notes from review results)
- blocked → blocked (with reason from failure)
- N/A → skipped (user chose to skip or abort)

## Handoff Data Between Stages

Implement → Spec Review:

- Implementer's self-report (what they claim)
- List of changed files (git diff --name-only)
- Task requirements from plan

Spec Review → Quality Review:

- Spec review verdict (must be PASS)
- Changed files list
- Project conventions reference

## Commit Expectations

Each implementation task produces exactly one commit (or a small number for complex tasks):

- Format: type(scope): subject
- Explicit file paths in git add
- No wildcards, no git add -A
- No AI footers (no Co-Authored-By lines)

# Report Templates Reference

## Step 5: Sync Report Template

```text
## Sync Report

### Root CLAUDE.md

~ react: 18.2.0 → 19.1.0 (line 8)
+ vitest: 3.1.0 (new, not documented)
- jest: removed from deps (line 12)
~ test command: "jest" → "vitest run" (line 22)

### Module: src/billing/CLAUDE.md

- src/billing/legacy.py referenced but deleted
+ src/billing/v2/ new subdirectory, not documented
~ entry point changed: BillingService → BillingV2Service

### Module: src/auth/CLAUDE.md

= No drift detected

### Rule: .claude/rules/api.md

~ paths glob "src/api/**" matches 0 files (directory renamed to src/endpoints/)

### Hierarchy Changes

+ src/notifications/ qualifies as Domain Boundary, no CLAUDE.md
- src/legacy/CLAUDE.md orphaned (directory has 0 source files)
```

## Step 8: Post-Sync Report Template

```text
## Sync Complete

### Updated Files

  Path                          Changes  Lines before → after
  ./CLAUDE.md                   3        82 → 80
  src/billing/CLAUDE.md         2        55 → 48
  .claude/rules/api.md          1        25 → 25

### Unresolved

+ src/notifications/ needs CLAUDE.md → /claudemd:init src/notifications
- src/legacy/CLAUDE.md orphaned → delete manually or /claudemd:optimize

### Context Load (post-sync)

Working in...              Total loaded
src/billing/               root (80) + billing (48) = 128/250

△ Review changes with `git diff` before committing.
```

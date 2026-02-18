# Report Template

```text
## CLAUDE.md Audit Report

### Summary

Files scanned: {COUNT} ({ROOT} root, {MODULE} module, {RULE} rules)
Max loaded at once: {MAX}/250 (working in {WORST_PATH})

Health: {HEALTHY | NEEDS_ATTENTION | CRITICAL}

### Findings

◆◆ ERROR: src/billing/CLAUDE.md duplicates root Commands section
   → Remove lines 12-18, root commands already loaded

◆◆ ERROR: Max context load is {N} lines when working in src/billing/stripe/
   → Condense billing module or move content to stripe sub-module

◆ WARNING: Stale root - package.json has react 19, CLAUDE.md says 18
   → Run /claudemd:sync

◆ WARNING: src/legacy/CLAUDE.md - directory has 1 file remaining
   → Remove orphaned module file

◇ INFO: src/middleware/ qualifies as Technical Complexity, no CLAUDE.md
   → Run /claudemd:init src/middleware

### Per-File Metrics

  Path                          Lines  Issues  Status
  ./CLAUDE.md                   {N}    {N}     ✓
  src/billing/CLAUDE.md         {N}    {N}     ◆
  src/auth/CLAUDE.md            {N}    {N}     ✓
  .claude/rules/testing.md      {N}    {N}     ✓

### Context Load Map

Working in...              Files loaded                Total
src/billing/               root + billing              {N}/250
src/billing/stripe/        root + billing + stripe     {N}/250
src/auth/                  root + auth                 {N}/250
(anywhere else)            root only                   {N}/250

### Recommended Actions

1. /claudemd:sync     → Fix {N} stale references
2. /claudemd:optimize → Reduce src/billing/CLAUDE.md from {N} to ~50 lines
3. /claudemd:init src/middleware → Generate missing module file
```

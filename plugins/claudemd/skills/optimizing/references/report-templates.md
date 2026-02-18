# Report Templates

## Step 3: Optimization Plan Template

```text
## Optimization Plan

Current worst-case load: {N}/250 lines (working in {WORST_PATH})
Target worst-case load: ~{N}/250 lines

### Changes by File

./CLAUDE.md ({N} → ~{N} lines)
  - Condense verbose sections (-{N})
  - Remove linter rules (-{N})

src/billing/CLAUDE.md ({N} → ~{N} lines)
  - Remove duplicated root content (-{N})
  - Extract stripe details to sub-module (-{N})

src/auth/CLAUDE.md ({N} → ~{N} lines)
  - Condense 3 paragraphs to table (-{N})
  - Replace inline example with file ref (-{N})

NEW: src/billing/stripe/CLAUDE.md (~{N} lines)
  - Extracted from oversized billing module

NEW: .claude/rules/validation.md (~{N} lines)
  - Cross-cutting rule extracted from 3 modules

DELETE: src/legacy/CLAUDE.md
  - Directory has 0 source files
```

Then prompt:

```yaml
AskUserQuestion:
  question: "Apply this optimization plan?"
  header: "Optimize"
  options:
    - label: "Apply all (Recommended)"
      description: "Execute all optimizations"
    - label: "Cherry-pick"
      description: "Choose which optimizations to apply"
    - label: "Preview only"
      description: "Show proposed file contents without writing"
```

## Step 5: Post-Optimization Report Template

```text
## Optimization Complete

### Before → After

  Path                          Before  After   Change
  ./CLAUDE.md                   {N}     {N}     -{N}
  src/billing/CLAUDE.md         {N}     {N}     -{N}
  src/billing/stripe/CLAUDE.md  -       {N}     +{N} (extracted)
  src/auth/CLAUDE.md            {N}     {N}     -{N}
  .claude/rules/validation.md   -       {N}     +{N} (cross-cutting)
  src/legacy/CLAUDE.md          {N}     -       removed

### Context Load Map (post-optimization)

Working in...              Before   After
src/billing/               {N}      {N}  (-{SAVED})
src/billing/stripe/        -        {N}  (new path)
src/auth/                  {N}      {N}  (-{SAVED})
(anywhere)                 {N}      {N}  (-{SAVED})

Worst case: {MAX}/250 (was {OLD_MAX})

△ Review with `git diff`. Run /claudemd:audit to validate.
```

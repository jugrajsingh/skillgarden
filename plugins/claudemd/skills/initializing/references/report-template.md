# Summary Report Template

After all files are generated, output this report:

```text
## Init Complete

### Files Generated

  Path                            Lines  Level        Criterion
✓ ./CLAUDE.md                     {N}    Root         -
✓ src/api/handlers/CLAUDE.md      {N}    Module       Integration point
✓ src/billing/CLAUDE.md           {N}    Module       Domain boundary
✓ src/billing/stripe/CLAUDE.md    {N}    Sub-module   Integration point
✓ src/auth/CLAUDE.md              {N}    Module       Domain boundary
✓ .claude/rules/testing.md        {N}    Rule         Cross-cutting
  CLAUDE.local.md                 {N}    Local        Personal (gitignored)

### Context Budget (per working directory)

Working in...              Loaded files               Total lines
src/billing/               root + billing             {N}
src/billing/stripe/        root + billing + stripe    {N}
src/auth/                  root + auth                {N}
(anywhere else)            root only                  {N}

Max loaded at once: {MAX}/250

### Next Steps

- Review: git diff
- Validate: /claudemd:audit
- Re-generate one dir: /claudemd:init {path}
```

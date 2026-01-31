# Knowledge Packs

Framework-specific diagnostic patterns used by the unstuck plugin.

## Naming Convention

`{language}-{framework}.md` — lowercase, hyphenated.

Examples: `python-fastapi.md`, `typescript-nextjs.md`, `go-grpc.md`, `rust-actix.md`

## Structure

Each knowledge file follows this template:

```markdown
# {Framework} Diagnostic Patterns

## Common Errors
| Error | Likely Cause | Check |
|-------|-------------|-------|

## Gotchas
- Framework-specific traps that waste debugging time

## Diagnostic Commands
- Framework-specific commands to gather evidence

## Known Patterns
- Recurring issues and their resolutions
```

## How Skills Use Knowledge Packs

Skills detect the language/framework from the error context and project files. If a matching `knowledge/{lang}-{framework}.md` exists, the skill reads it and applies framework-specific patterns before generic debugging.

## Contributing

1. Create `{language}-{framework}.md` following the structure above
2. Focus on non-obvious errors — skip things any developer would know
3. Include exact error messages where possible (helps pattern matching)
4. Keep diagnostic commands copy-pasteable

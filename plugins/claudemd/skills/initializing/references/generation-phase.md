# Phase 3: Generation — Detailed Instructions

## 3a. Generate Root CLAUDE.md

Use the WHAT-WHY-HOW framework. Each section earns its place.

```markdown
# {PROJECT_NAME}

{ one-line purpose }

## Tech Stack

{ only non-obvious versions/tools }

## Structure

{ key directories with 2-3 word purpose annotations }
{ only directories Claude needs to navigate }

## Commands

{ build, test, lint with exact syntax }
{ skip obvious ones like `npm install` }

## Conventions

{ project-specific patterns and anti-patterns }
{ not language/framework defaults }

## Gotchas

{ things that break, workarounds, non-obvious behavior }
```

**Omit a section if it would only state the obvious.**

| Section | Include when... |
|---------|----------------|
| Tech Stack | Non-obvious versions, custom tooling |
| Structure | >5 directories with distinct purposes |
| Commands | Build/test commands aren't self-evident |
| Conventions | Project deviates from framework defaults |
| Gotchas | Known pitfalls exist |

## 3b. Generate Module CLAUDE.md Files (Parallel)

Read the root CLAUDE.md first. All subagents need this context.

For each target, spawn a `Task(general-purpose)` subagent:

```text
Task for {target.path}:

CONTEXT: The root CLAUDE.md contains:
---
{root_claude_md_content}
---

Create {target.path}/CLAUDE.md. This file autoloads when Claude works
in {target.path}/. It COMPLEMENTS the root (always loaded). Never
repeat what root covers.

INCLUDE:

1. Module purpose - one line: what this directory is and does
2. Architecture - how components relate (big picture requiring
   multiple files to understand)
3. Local commands - subdirectory-specific test/build paths or flags
4. Conventions - patterns unique to THIS directory
5. Gotchas - non-obvious behavior, pitfalls, workarounds
6. Key interfaces - entry points, public API surface

EXCLUDE:

- Anything the root CLAUDE.md covers
- Generic practices ("write tests", "handle errors")
- Exhaustive file listings (discoverable via ls)
- Framework patterns Claude already knows
- Made-up sections with no real content
- Code style rules handled by linters

CONSTRAINTS:

- Under 80 lines
- No section with fewer than 2 actionable items
- Reference canonical files instead of inline code examples
- If CLAUDE.md exists, suggest improvements vs creating new
```

**Dispatch all subagents in a single message for parallel execution.**

## 3c. Generate Cross-Cutting Rules (Optional)

If the codebase has conventions that span multiple modules but only apply to specific file types, create `.claude/rules/` files:

```markdown
---
paths:
  - "**/*.test.{ts,py}"
---

# Test Conventions

{ rules that apply to ALL test files across modules }
```

Use `.claude/rules/` ONLY for cross-cutting concerns. Module-specific content goes in module CLAUDE.md.

| Mechanism | When to use |
|-----------|-------------|
| Module CLAUDE.md | Domain-specific: architecture, local patterns, integration contracts |
| .claude/rules/ | Cross-cutting: test conventions, API style, security rules across all modules |

## 3d. Generate CLAUDE.local.md Template

```bash
grep -q 'CLAUDE.local.md' .gitignore 2>/dev/null || echo "CLAUDE.local.md" >> .gitignore
```

## 3e. Post-Generation Validation

For each generated file:

- [ ] Within size target for its level
- [ ] No duplication with root CLAUDE.md
- [ ] No secrets, credentials, or API keys
- [ ] No code style rules that linters handle
- [ ] No framework basics Claude already knows
- [ ] No section with fewer than 2 actionable items

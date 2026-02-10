---
name: auditing
description: Audit a skill against design best practices - structure, modularization, token efficiency, reference file patterns, and known gotchas.
allowed-tools:
  - Read
  - Glob
  - Grep
  - AskUserQuestion
---

# Audit Skill Design

Evaluate a skill's SKILL.md and reference files against best practices for structure, modularization, and token efficiency.

## Workflow

### 1. Locate the Skill

If path provided, read it directly. Otherwise:

```text
Glob: **/skills/*/SKILL.md
```

Ask user which skill to audit via AskUserQuestion.

### 2. Read Skill Files

Read the SKILL.md and list any `references/` directory contents:

```text
Glob: {skill_dir}/references/*.md
```

### 3. Measure Token Budget

Count SKILL.md lines. Reference: every SKILL.md line costs tokens on every invocation.

| Lines | Rating | Action |
|-------|--------|--------|
| < 200 | Good | No action needed |
| 200-400 | Watch | Consider if all content is always needed |
| 400-500 | Extract | Identify conditionally-loaded sections |
| > 500 | Over budget | Must extract to references |

### 4. Check Structure

Read `references/structure.md` for the structural checklist.

### 5. Check Modularization

Read `references/modularization.md` for the reference file pattern checklist.

### 6. Check Gotchas

Read `references/gotchas.md` for known pitfalls.

### 7. Report

```text
============================================================================
Skill Audit: {plugin}:{skill}
============================================================================

Token Budget:
  SKILL.md: {lines} lines ({rating})
  References: {count} files, {total_lines} lines (loaded conditionally)

Structure:                                          Score
  ✓/✗ Frontmatter complete                         {pass/fail}
  ✓/✗ Skill has allowed-tools                        {pass/fail}
  ✓/✗ Workflow numbered steps                      {pass/fail}
  ✓/✗ Detection before generation                  {pass/fail}
  ✓/✗ User confirmation before action              {pass/fail}
  ✓/✗ Report section at end                        {pass/fail}

Modularization:                                     Score
  ✓/✗ No unconditional large blocks               {pass/fail}
  ✓/✗ References used for variant content          {pass/fail}
  ✓/✗ References loaded conditionally              {pass/fail}
  ✓/✗ No repeated content across references        {pass/fail}

Gotchas:                                            Score
  ✓/✗ No backticks around shell metacharacters     {pass/fail}
  ✓/✗ No name collision (command vs skill)         {pass/fail}
  ✓/✗ Variables use correct placeholder syntax     {pass/fail}
  ✓/✗ ASCII indicators (no emoji)                  {pass/fail}

Findings:
  {severity} {description}
  ...

Recommendations:
  {numbered_list}
============================================================================
```

## Reference Files

- `references/structure.md` - Skill structure checklist
- `references/modularization.md` - Reference file patterns and when to extract
- `references/gotchas.md` - Known pitfalls in skill authoring

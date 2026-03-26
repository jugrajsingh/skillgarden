---
name: brainstorming
description: Use when designing new features, architecture decisions, refactor strategies, or decomposing complex problems through iterative questioning
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash(git *)
  - Bash(mkdir *)
  - AskUserQuestion
---

# Design Brainstorming

Explore design ideas through iterative questioning, trade-off analysis, and structured design doc output.

HARD-GATE: Do NOT invoke any implementation skill, write code, or scaffold files until the design doc is approved by the user. Even for trivially simple projects — design first, always.

## Input

`$ARGUMENTS` = feature idea or problem statement.

If `$ARGUMENTS` is empty, ask:

```yaml
AskUserQuestion:
  question: "What would you like to brainstorm?"
  header: "Topic"
  options:
    - label: "New feature"
      description: "Design a new capability from scratch"
    - label: "Architecture decision"
      description: "Evaluate structural approaches for a system concern"
    - label: "Refactor strategy"
      description: "Plan how to restructure existing code"
    - label: "Problem decomposition"
      description: "Break down a complex problem into manageable parts"
```

## Step 1: Check Project State

Gather context before asking questions:

```bash
git log -5 --oneline
```

```bash
ls docs/plans/ 2>/dev/null
```

Read README.md (or README) if it exists for project context.

Scan docs/plans/ for any existing design docs related to the topic. If a relevant design already exists, mention it and ask whether to extend or start fresh.

### Scope Decomposition Check

If the request spans multiple independent subsystems, flag it immediately:

```yaml
AskUserQuestion:
  question: "This spans multiple independent subsystems. Design each separately?"
  header: "Scope"
  options:
    - label: "Yes, decompose"
      description: "Create separate design docs per subsystem"
    - label: "No, single design"
      description: "Treat as one unified design"
```

If decomposed: run brainstorming once per subsystem, each with its own design doc.

### Existing Codebase Awareness

When working in an existing codebase: explore first, follow existing patterns, include targeted improvements for code you touch, never propose unrelated refactoring.

## Step 2: Ask Clarifying Questions

Ask up to 3 questions **one at a time** via AskUserQuestion: who benefits (users/developers/ops), constraints (integration/performance/time), scope (minimal/focused/broad). Skip questions already answered by context.

See references/question-flows.md for the AskUserQuestion YAML blocks.

## Step 3: Propose Approaches

Propose 2-3 meaningfully different approaches with trade-offs (pro/con for each). Present via AskUserQuestion for selection. See references/question-flows.md for approach proposal format.

## Step 4: Iterate on Chosen Approach

Refine selected approach. Up to 3 rounds: identify uncertain aspects, ask targeted question, incorporate answer. After each round offer: write it up, needs refinement, or start over. See references/question-flows.md for iteration check.

## Step 5: Generate Design Doc

Generate slug (lowercase, hyphenated, max 5 words).

```bash
mkdir -p docs/plans/{SLUG}
```

Create `docs/plans/{SLUG}/design.md`. Scale section depth to complexity — simple features get brief docs, complex systems get thorough ones.

See references/design-doc-template.md for the full template including interface contracts.

## Step 6: Spec Self-Review

Before presenting to user, automatically review the design doc:

1. **Placeholder scan** — search for `{`, `TODO`, `TBD`, `???`. Fix inline.
2. **Internal consistency** — method names, data types, and component names used consistently throughout.
3. **Scope check** — every section traces back to a stated goal. Remove scope creep.
4. **Ambiguity check** — flag vague phrases ("as needed", "where appropriate", "etc.") and replace with specifics.

Fix all issues inline. Do not present a doc with known defects.

## Step 7: User Review Gate

Present the design doc and explicitly ask for approval:

```yaml
AskUserQuestion:
  question: "Design doc written. Please review and approve before proceeding."
  header: "Approval"
  options:
    - label: "Approved"
      description: "Design is solid, proceed to next steps"
    - label: "Needs changes"
      description: "I have feedback to incorporate"
    - label: "Restart"
      description: "Start over with a different approach"
```

If "Needs changes": incorporate feedback, re-run self-review, present again.
If "Restart": return to Step 3.

## Step 8: Commit Design Doc

After approval, commit the design doc to git:

```bash
git add docs/plans/{SLUG}/design.md
```

```bash
git commit -m "docs(plans): add {SLUG} design doc"
```

## Step 9: Offer Next Steps

Offer: create worktree (`planner:worktrees`), create implementation plan (`planner:planning`), or done. See references/question-flows.md for next steps format.

The ONLY planning skill to invoke after brainstorming is `planner:planning`.

## Rules

- One question at a time — never batch multiple questions
- Never assume requirements — always confirm with the user
- Design docs are proposals until approved — mark status as "proposal", change to "approved" after gate
- If an existing design doc covers the topic, surface it before starting fresh
- Always offer concrete next steps at the end
- HARD-GATE: No implementation, code, or scaffolding until design is approved
- Design for isolation and clarity — well-bounded units with clear interfaces. You reason better about code you can hold in context at once.

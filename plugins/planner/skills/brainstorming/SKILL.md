---
name: brainstorming
description: Use when designing new features, architecture decisions, refactor strategies, or decomposing complex problems through iterative questioning
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
---

# Design Brainstorming

Explore design ideas through iterative questioning, trade-off analysis, and structured design doc output.

## Input

`$ARGUMENTS` = feature idea or problem statement.

If `$ARGUMENTS` is empty, ask:

```yaml
AskUserQuestion:
  question: "What would you like to brainstorm?"
  header: "Brainstorm Topic"
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

## Step 2: Ask Clarifying Questions

Ask up to 3 questions **one at a time** via AskUserQuestion: who benefits (users/developers/ops), constraints (integration/performance/time), scope (minimal/focused/broad). Skip questions already answered by context.

See references/question-flows.md for the AskUserQuestion YAML blocks.

## Step 3: Propose Approaches

Propose 2-3 meaningfully different approaches with trade-offs (pro/con for each). Present via AskUserQuestion for selection. See references/question-flows.md for approach proposal format.

## Step 4: Iterate on Chosen Approach

Refine selected approach. Up to 3 rounds: identify uncertain aspects, ask targeted question, incorporate answer. After each round offer: write it up, needs refinement, or start over. See references/question-flows.md for iteration check.

## Step 5: Generate Design Doc

Generate slug (lowercase, hyphenated, max 5 words). Create `docs/plans/{SLUG}-design.md` with overview, goals, non-goals, approach, key decisions, trade-offs, and open questions. Keep under 200 lines. See references/design-doc-template.md.

## Step 6: Offer Next Steps

Offer: create worktree (`planner:worktrees`), create implementation plan (`planner:planning`), or done. See references/question-flows.md for next steps format.

## Rules

- One question at a time — never batch multiple questions
- Never assume requirements — always confirm with the user
- Design docs are proposals, not commitments — mark status as "proposal"
- Keep design docs under 200 lines
- If an existing design doc covers the topic, surface it before starting fresh
- Always offer concrete next steps at the end

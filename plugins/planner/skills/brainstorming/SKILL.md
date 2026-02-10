---
name: brainstorming
description: Design exploration through guided dialogue — iterative questioning, trade-off analysis, design doc output
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

Ask up to 3 clarifying questions, **one at a time**, using AskUserQuestion with multiple-choice options where possible.

**Question 1 — Who benefits:**

```yaml
AskUserQuestion:
  question: "Who is the primary user or beneficiary of this?"
  header: "Target User"
  options:
    - label: "End users"
      description: "People using the product directly"
    - label: "Developers"
      description: "Engineers working on the codebase"
    - label: "Operations"
      description: "Team managing deployment and infrastructure"
    - label: "Other"
      description: "Describe in your response"
```

**Question 2 — Constraints:**

```yaml
AskUserQuestion:
  question: "What constraints should we consider?"
  header: "Constraints"
  options:
    - label: "Must integrate with existing system"
      description: "Cannot rewrite or replace current components"
    - label: "Performance-critical"
      description: "Latency, throughput, or resource limits matter"
    - label: "Time-boxed"
      description: "Must ship within a fixed timeframe"
    - label: "No major constraints"
      description: "Greenfield or flexible scope"
```

**Question 3 — Scope:**

```yaml
AskUserQuestion:
  question: "What scope feels right for a first iteration?"
  header: "Scope"
  options:
    - label: "Minimal — proof of concept"
      description: "Smallest version that validates the idea"
    - label: "Focused — single use case"
      description: "One complete workflow end-to-end"
    - label: "Broad — multiple use cases"
      description: "Cover the main scenarios from the start"
```

Skip questions whose answers are already clear from `$ARGUMENTS` or project context.

## Step 3: Propose Approaches

Based on answers, propose 2-3 approaches with trade-offs.

Present via AskUserQuestion:

```yaml
AskUserQuestion:
  question: "Which approach resonates most? We can refine from there."
  header: "Proposed Approaches"
  options:
    - label: "{APPROACH_1_NAME}"
      description: "{1-sentence summary}. Pro: {benefit}. Con: {drawback}"
    - label: "{APPROACH_2_NAME}"
      description: "{1-sentence summary}. Pro: {benefit}. Con: {drawback}"
    - label: "{APPROACH_3_NAME}"
      description: "{1-sentence summary}. Pro: {benefit}. Con: {drawback}"
```

Each approach should be meaningfully different, not minor variations.

## Step 4: Iterate on Chosen Approach

Refine the selected approach. Up to 3 iteration rounds.

Each round:

1. Identify the most uncertain or underspecified aspect
2. Ask a targeted question via AskUserQuestion
3. Incorporate the answer into the design

After each round, offer:

```yaml
AskUserQuestion:
  question: "How does this look?"
  header: "Design Check"
  options:
    - label: "Looks good — write it up"
      description: "Converge on this design and generate the doc"
    - label: "Needs refinement"
      description: "I have feedback or concerns to address"
    - label: "Start over with different approach"
      description: "Switch to a different approach from Step 3"
```

If "Looks good" is selected, proceed to Step 5. If "Start over" is selected, return to Step 3.

## Step 5: Generate Design Doc

Generate a slug from the feature name (lowercase, hyphenated, max 5 words).

```bash
mkdir -p docs/plans
```

Create `docs/plans/{SLUG}-design.md` with:

```markdown
# Design: {TITLE}

**Date:** {TODAY}
**Status:** proposal

## Overview

{ 2-3 sentence summary of the feature and chosen approach }

## Goals

- { what this design achieves }
- { measurable outcomes where possible }

## Non-Goals

- { explicitly out of scope items }
- { things this design does NOT address }

## Approach

{ detailed description of the chosen approach }

### Key Decisions

- { decision 1 }: { rationale }
- { decision 2 }: { rationale }

## Trade-offs Considered

| Option | Pros | Cons | Verdict |
|--------|------|------|---------|
| {APPROACH_1} | {pros} | {cons} | {chosen/rejected} |
| {APPROACH_2} | {pros} | {cons} | {chosen/rejected} |

## Open Questions

- { unresolved question 1 }
- { unresolved question 2 }
```

Keep design docs under 200 lines.

## Step 6: Offer Next Steps

```yaml
AskUserQuestion:
  question: "What would you like to do next?"
  header: "Next Steps"
  options:
    - label: "Create worktree"
      description: "Set up isolated branch for this feature"
    - label: "Create implementation plan"
      description: "Decompose into tasks with 3-file persistence"
    - label: "Done for now"
      description: "Save design doc and stop here"
```

- "Create worktree" — load the `planner:worktrees` skill, passing the slug as branch name
- "Create implementation plan" — load the `planner:planning` skill, passing the design doc path
- "Done for now" — report design doc path and exit

## Rules

- One question at a time — never batch multiple questions
- Never assume requirements — always confirm with the user
- Design docs are proposals, not commitments — mark status as "proposal"
- Keep design docs under 200 lines
- If an existing design doc covers the topic, surface it before starting fresh
- Always offer concrete next steps at the end

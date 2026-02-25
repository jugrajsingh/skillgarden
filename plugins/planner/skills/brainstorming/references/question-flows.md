# Brainstorming Question Flows

## Step 2: Clarifying Questions

Ask up to 3 questions **one at a time** via AskUserQuestion. Skip questions whose answers are clear from arguments or project context.

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

## Step 3: Approach Proposal

Present 2-3 meaningfully different approaches:

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

## Step 4: Iteration Check

After each refinement round:

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

## Step 6: Next Steps

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

- "Create worktree" — load the `planner:worktrees` skill
- "Create implementation plan" — load the `planner:planning` skill
- "Done for now" — report design doc path and exit

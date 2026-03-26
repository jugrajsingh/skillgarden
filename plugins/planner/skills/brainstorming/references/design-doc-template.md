# Design Doc Template

Create `docs/plans/{SLUG}/design.md` with:

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

## Interface Contracts

Define boundaries between components. Each contract specifies inputs, outputs,
and the agreement between caller and callee.

### { Component A } -> { Component B }

**Method/Endpoint:** { signature or path }
**Input:** { data schema or parameters }
**Output:** { return type or response shape }
**Errors:** { error cases and how they surface }
**Invariants:** { what must always be true }

{ Repeat for each boundary }

## Trade-offs Considered

| Option | Pros | Cons | Verdict |
|--------|------|------|---------|
| {APPROACH_1} | {pros} | {cons} | {chosen/rejected} |
| {APPROACH_2} | {pros} | {cons} | {chosen/rejected} |

## Open Questions

- { unresolved question 1 }
- { unresolved question 2 }
```

Scale section depth to complexity. Simple features may skip Interface Contracts.
Complex multi-component designs should define every boundary.

No hard line limit — clarity over brevity. But avoid padding.

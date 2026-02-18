# Research Report Format

## YAML Frontmatter

```yaml
---
question: {original research question}
date: {YYYY-MM-DD}
agents: [locator, analyzer, pattern-finder]
status: complete | partial | inconclusive
---
```

Status meanings:

| Status | Meaning |
|--------|---------|
| complete | All sub-questions answered with citations |
| partial | Some sub-questions unanswered or missing citations |
| inconclusive | Conflicting findings or insufficient evidence |

## _OVERVIEW Section

2-3 sentence direct answer to the original question. No hedging. If uncertain, state what IS known and what IS NOT.

## Detail Sections

One section per sub-question. Each section must include:

- Section header matching the sub-question
- Findings with file:line citations
- Code snippets where relevant (max 20 lines each)
- Agent attribution (which agent produced this finding)

## Cross-References

Link related findings across sections. Example:

```text
The auth middleware (see Section 2) uses the token format defined in Section 3.
```

## Gaps Section

What could not be determined and why. Include:

- Unanswered aspects of the original question
- Files that could not be located
- Suggested next steps for further investigation

## Output Summary

```text
## Research Complete

Report: docs/research/{slug}-report.md
Status: {status}
Agents: {count} dispatched, {count} successful

### Key Findings
- {finding 1 with file:line}
- {finding 2 with file:line}
- {finding 3 with file:line}

### Gaps
- {gap 1}
```

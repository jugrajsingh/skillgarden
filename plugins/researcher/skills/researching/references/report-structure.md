# Research Report Structure

## YAML Frontmatter

```yaml
---
question: {original question}
date: {YYYY-MM-DD}
agents: [locator, analyzer, pattern-finder]
status: complete | partial | inconclusive
related_plan: {slug} (optional)
---
```

## Required Sections

### _OVERVIEW

2-3 sentence direct answer. No hedging. If uncertain, state what IS known and what IS NOT.

### Detail Sections

One per sub-question investigated. Each must include:

- Section header matching the sub-question
- Findings with file:line citations
- Code snippets where relevant (max 20 lines each)

### Cross-References

Links between related findings across sections. Example:

```text
The auth middleware (see Section 2) uses the token format defined in Section 3.
```

### Gaps

What could not be determined and why. Suggests next steps for further investigation.

## Citation Format

Always use `path/to/file.py:42` format — never just a filename without line number.

For ranges: `path/to/file.py:10-25`

For multiple references on one finding: `path/to/file.py:42, path/to/other.py:15`

## Progressive Disclosure

Structure from general to specific:

1. _OVERVIEW (answer in 2-3 sentences)
2. Section summaries (1 paragraph each)
3. Detailed findings (with code snippets)
4. Gaps and next steps

## Status Definitions

| Status | Criteria |
|--------|----------|
| complete | All sub-questions answered, all claims have file:line citations |
| partial | Some sub-questions unanswered or citations missing |
| inconclusive | Conflicting findings or insufficient evidence to answer |

## Agent Attribution

Each detail section should note which agent produced the findings:

```text
### How does the login flow work?
**Agent:** analyzer

{findings here}
```

## Code Snippet Rules

- Max 20 lines per snippet
- Include surrounding context (imports, class definition) for clarity
- Always cite exact file:line range above the snippet
- Use the actual language for syntax highlighting

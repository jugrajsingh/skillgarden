# Phase 2: Judgment — Detailed Criteria

Identify which directories warrant their own CLAUDE.md.

**Root always gets a CLAUDE.md.** For all other directories, apply the four semantic criteria.

## Qualification Criteria

A directory qualifies if it matches ANY of:

| Criterion | What to look for |
|-----------|-----------------|
| **Domain Boundary** | Cohesive files forming a distinct conceptual area. Someone would work "in this domain." Examples: auth, billing, search |
| **Integration Point** | Connects to external systems. Filenames suggest: webhook, client, adapter, provider, gateway |
| **Sub-App** | Self-contained with entry points, routes, or own runtime. Could be extracted as standalone |
| **Technical Complexity** | Non-obvious patterns an agent would get wrong without local guidance |

## Two Critical Rules

### Rule 1: Children Over Parent

When parent qualifies, check if children also qualify. If children qualify, generate for EACH child and SKIP the parent.

```text
src/api/           → SKIP (children cover it)
src/api/handlers/  → ✓ Integration point
src/api/middleware/ → ✓ Technical complexity
```

### Rule 2: Semantic Citation

Cite which criterion applies for each target. No "other" category. If none apply, the directory does not need a CLAUDE.md.

## Exclusion Signals

Skip directories that are:

- Pure utility/helper collections (string utils, math helpers)
- Auto-generated code directories
- Test directories that mirror source structure
- Vendor/dependency directories
- Directories with <3 files and no manifest

## Judgment Output

```text
## Targets

  #  Path                    Criterion
  0  ./                      Root (always)
  1  src/api/handlers/       Integration point
  2  src/billing/            Domain boundary
  3  src/billing/stripe/     Integration point
  4  src/auth/               Domain boundary

Skipped:
- src/utils/ (utility collection)
- src/api/ (children cover it)
```

```yaml
AskUserQuestion:
  question: "Generate CLAUDE.md for these directories?"
  header: "Targets"
  options:
    - label: "All targets (Recommended)"
      description: "Generate root + {N} module files"
    - label: "Select targets"
      description: "Choose which directories to include"
    - label: "Root only"
      description: "Generate only root CLAUDE.md"
```

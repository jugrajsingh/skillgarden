# Detection Methods

## Dead Code Detection

For each file in scope:

**Unreferenced functions/classes:**

- Find all function/class definitions (def, class, function, const, export)
- For each definition, search the rest of the codebase for references
- If zero references outside the definition file (excluding tests), flag it
- Exception: entry points (main, **main**, CLI handlers, exports in **init**.py)

**Unused imports:**

- Extract all import statements
- Check if imported name appears elsewhere in the file
- Flag imports where the name is never used after the import line

**Commented-out code:**

- Detect blocks of 3+ consecutive comment lines containing code patterns
- Code patterns: def, class, if, for, while, return, import, from, =, ()
- Single-line comments explaining logic are NOT dead code

Report format per finding: `file:line | type | description`

## Duplication Scan

**Function-level duplication:**

- Compare function signatures across files in scope
- Flag functions with identical names and similar parameter counts in different files

**Block-level duplication:**

- Identify code blocks (5+ lines) that appear nearly identical in multiple locations
- "Nearly identical" = same structure, possibly different variable names
- Use grep to find repeated patterns (string literals, logic sequences)

Report format: `fileA:line <-> fileB:line | description`

## Staleness Check

**File staleness:**

```bash
git log --oneline -50 --format="%H" | tail -1
```

Use the 50th commit as the cutoff. Find files not modified since:

```bash
git log -1 --format="%ai" -- {FILE}
```

Compare against cutoff commit date.

**Outdated documentation:**

- Find .md files referencing paths or function names that no longer exist
- Check internal links in documentation files

**Old TODOs:**

- Search for TODO, FIXME, HACK comments
- Check git blame for each to determine age
- Flag those older than 20 commits from HEAD

Report format: `file | last modified | description`

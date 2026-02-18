# Cleanup Phase Details

## Phase 3: Remove Dead Code

For each approved removal, execute in order:

### Unused Imports

1. Read the file
2. Remove the import line(s)
3. If import was part of a grouped import (e.g., `from x import a, b, c`), remove only the unused name
4. Verify: grep the file for the removed name to confirm it's truly unused

### Unreferenced Functions/Classes

1. Read the file
2. Identify the full extent of the function/class (definition through last line)
3. Remove the entire definition including decorators and docstring
4. Verify: grep the codebase for the function/class name
5. If any reference found outside the original location, STOP and report to user

### Commented-Out Code

1. Read the file
2. Remove the consecutive comment block identified in assessment
3. Preserve any non-code comments (explanatory text) adjacent to the block

After each removal:

```bash
# Sanity check — search for broken references
grep -r "removed_name" --include="*.py" --include="*.ts" --include="*.js" .
```

If references found, revert the change and report to user.

## Phase 4: Consolidate Duplicates

For each approved consolidation:

### Identify Canonical Location

Decision criteria:

- Prefer the more complete implementation
- Prefer the file closer to shared/utils in the directory tree
- If equal, prefer the older version (first committed)

### Extract and Deduplicate

1. Read both files containing duplicate code
2. Choose canonical location
3. If both files import from the same parent module:
   - Extract to a shared utility in the common parent
   - Update both files to import from the shared location
4. If files are in different modules:
   - Keep the version in the more appropriate location
   - Replace the other with an import/reference to the canonical version
5. Update all call sites across the codebase

After each consolidation:

```bash
# Verify all references resolve
grep -rn "function_name" --include="*.py" --include="*.ts" --include="*.js" .
```

## Phase 5: Archive Stale Content

CRITICAL: Never delete files. Always archive.

### Setup Archive Directory

```bash
mkdir -p .archive
```

If .archive is not in .gitignore, warn the user and suggest adding it.

### Archive Process

For each approved archive:

1. Create the mirrored directory structure:

   ```bash
   mkdir -p .archive/{original-directory-path}
   ```

2. Move the file:

   ```bash
   git mv {original-path} .archive/{original-path}
   ```

   If not git-tracked, use regular mv.

3. Update references:
   - Search for any imports, links, or references to the archived file
   - Update or annotate them with the new archive location
   - If a reference is in active code (not docs), warn user instead of auto-updating

### Archive Manifest

After all archives, create or update `.archive/MANIFEST.md`:

```text
# Archive Manifest

| Original Path | Archived Date | Reason |
|---------------|---------------|--------|
| docs/old-api.md | {DATE} | Stale — not modified in 80 commits |
```

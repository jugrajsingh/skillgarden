# Phase 1: Discovery — Detailed Steps

Build a metadata-rich directory tree from git-tracked files.

## 1a. Check Existing State

```bash
find . -name 'CLAUDE.md' -not -path '*/node_modules/*' -not -path '*/venv/*' 2>/dev/null
ls .claude/rules/*.md 2>/dev/null
```

If root CLAUDE.md exists, ask:

```yaml
AskUserQuestion:
  question: "Existing CLAUDE.md files found. How should I proceed?"
  header: "Existing files"
  options:
    - label: "Regenerate all"
      description: "Fresh analysis, overwrite existing files"
    - label: "Fill gaps"
      description: "Keep existing, generate only for directories missing CLAUDE.md"
    - label: "Cancel"
      description: "Abort without changes"
```

## 1b. Structure Mining

```bash
git ls-files | xargs -n1 dirname | sort | uniq -c | sort -rn
```

For each directory, capture:

| Field | Source |
|-------|--------|
| `path` | Directory path |
| `file_count` | Direct files in this directory |
| `subtree_count` | Total files in subtree |
| `has_manifest` | Contains package.json, go.mod, Cargo.toml, pyproject.toml, Gemfile, pom.xml |
| `has_claude_md` | Already has CLAUDE.md |

```bash
find . -maxdepth 4 \( -name 'package.json' -o -name 'go.mod' -o -name 'Cargo.toml' -o -name 'pyproject.toml' -o -name 'Gemfile' -o -name 'pom.xml' \) -not -path '*/node_modules/*' 2>/dev/null
```

## 1c. Codebase Signals (parallel)

**Tech stack:**

```bash
cat package.json 2>/dev/null | head -30
cat pyproject.toml 2>/dev/null | head -30
cat go.mod 2>/dev/null | head -10
```

**Build/test/lint commands:**

```bash
jq -r '.scripts | keys[]' package.json 2>/dev/null
cat Makefile 2>/dev/null | grep -E '^[a-zA-Z_-]+:' | head -20
```

**Existing conventions:**

```bash
ls .editorconfig .eslintrc* .prettierrc* ruff.toml biome.json .pre-commit-config.yaml 2>/dev/null
```

**Git context:**

```bash
git log --oneline -10
git remote -v 2>/dev/null | head -2
```

## 1d. Semantic Enrichment (Optional)

For directories with 3+ files, read 2-3 representative files and note:

- Exported symbols: class names, function names, type names
- Domain hints from naming (e.g., `AuthService` → auth domain)

Skip if repo is small (<30 files total).

## Discovery Output

```text
## Directory Tree

Path                          Files  Subtree  Manifest  CLAUDE.md
./                            5      142      package   -
src/                          3      120      -         -
src/api/                      5      38       -         -
src/api/handlers/             12     12       -         -
src/billing/                  8      22       package   -
src/auth/                     14     14       -         -
src/utils/                    4      4        -         -
```

# Drift Analysis Reference

## Step 3: Analyze Codebase (Current Truth)

Run these in parallel:

**a) Tech stack:**

```bash
cat package.json 2>/dev/null | jq '{name, dependencies, devDependencies}' 2>/dev/null
cat pyproject.toml 2>/dev/null
cat go.mod 2>/dev/null | head -20
cat Cargo.toml 2>/dev/null | head -30
```

**b) Directory structure:**

```bash
git ls-files | xargs -n1 dirname | sort -u
```

**c) Available commands:**

```bash
jq -r '.scripts | to_entries[] | "\(.key): \(.value)"' package.json 2>/dev/null
cat Makefile 2>/dev/null | grep -E '^[a-zA-Z_-]+:' 2>/dev/null
```

**d) Linter/formatter config:**

```bash
ls .editorconfig .eslintrc* .prettierrc* ruff.toml biome.json .flake8 .rubocop.yml 2>/dev/null
```

**e) Module-level changes:**

For each module CLAUDE.md, check its directory:

```bash
# Files in module directory vs what module documents
find {module_path} -maxdepth 1 -type f | head -30
```

**f) Staleness signals:**

```bash
# For each context file, compare its last commit to codebase changes
find . -name 'CLAUDE.md' -not -path '*/node_modules/*' -exec sh -c 'echo "$(git log --format=%ci -1 -- "$1" 2>/dev/null) $1"' _ {} \;
git log --format=%ci -1 -- package.json pyproject.toml Makefile 2>/dev/null
```

## Step 4: Compute Diff (Per File)

For EACH context file, compare documented state vs reality:

**Root drift dimensions:**

| Dimension | Source of Truth | Documented In |
|-----------|----------------|---------------|
| Dependencies | package.json / pyproject.toml | Tech Stack section |
| Directories | Filesystem + git ls-files | Structure section |
| Commands | package.json scripts / Makefile | Commands section |

**Module drift dimensions:**

| Dimension | Source of Truth | Documented In |
|-----------|----------------|---------------|
| Module files | Filesystem | Architecture / structure references |
| Entry points | Source code exports | Key interfaces section |
| Local commands | Package scripts / Makefile targets | Commands section |

**Rule drift dimensions:**

| Dimension | Source of Truth | Documented In |
|-----------|----------------|---------------|
| Path globs | Filesystem | YAML frontmatter `paths:` |
| Cross-cutting conventions | Codebase patterns | Rule content |

**Change classification:**

| Symbol | Meaning |
|--------|---------|
| + | New in codebase, not documented |
| - | Documented but no longer exists |
| ~ | Changed (version, path, name) |

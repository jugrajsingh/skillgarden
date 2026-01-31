---
name: changelog
description: Generate changelog from git commits following Keep a Changelog format
---

# Changelog Generation

Generate structured changelog from commits.

## Usage

```text
/gitmastery:changelog           # Since last tag
/gitmastery:changelog v1.2.0    # Since specific tag
```

## Workflow

### 1. Get Commits

```bash
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
git log $LAST_TAG..HEAD --format="%H|%s|%an" --reverse
```

### 2. Map to Sections

| Type | Section |
|------|---------|
| feat | Added |
| fix | Fixed |
| perf, refactor | Changed |
| BREAKING | Changed (Breaking) |
| security | Security |
| deprecate | Deprecated |
| remove | Removed |

**Excluded:** chore, build, ci, test

### 3. Generate Output

```markdown
## [Unreleased] - YYYY-MM-DD

### Added
- New user authentication system (#123)
- Email verification for new users

### Changed
- **BREAKING**: API endpoint changed from /v1 to /v2
- Optimized database queries

### Fixed
- Memory leak in WebSocket connections (#167)
```

### 4. Ask User

```yaml
AskUserQuestion:
  question: "Write changelog to CHANGELOG.md?"
  options:
    - "Yes - prepend to file"
    - "Preview only"
    - "Cancel"
```

## Version Suggestion

Based on changes:

- **MAJOR** - Breaking changes (! suffix or BREAKING CHANGE footer)
- **MINOR** - New features (feat: type)
- **PATCH** - Fixes only (fix:, perf: types)

## Quality Rules

- Concise: <72 chars per entry
- Imperative: "Add feature" not "Added"
- User-focused: Impact, not implementation
- Skip generic: WIP, temp commits

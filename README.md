# SkillGarden

A plugin marketplace for Claude Code that brings discipline to your git workflow. No more accidental wildcard commits, no more forgotten conventional commit formats, no more AI footers cluttering your history.

## How It Works

SkillGarden plugins use **hooks** to enforce best practices automatically. When you try to `git add .` or commit with a bad message, the hook catches it *before* execution and guides you to the right approach.

The magic is in the combination:

- **PreToolUse hooks** intercept commands before they run
- **Skills** provide guided workflows with user confirmation
- **Commands** give you quick access via `/plugin:command`

You don't need to remember the rules. The plugins remember for you.

## Available Plugins

### gitmastery

Git workflow validation that actually works. Enforces explicit file staging, conventional commits, and blocks AI footers.

**What it blocks:**

- `git add .` or `git add *.py` → "List files explicitly"
- `git commit -m "fixed stuff"` → "Use conventional format: type(scope): subject"
- AI footers like `Co-Authored-By: Claude` → Blocked automatically

**Commands:**

| Command | Description |
|---------|-------------|
| `/gitmastery:commit` | Atomic commits with conventional format |
| `/gitmastery:feature` | Start a feature branch |
| `/gitmastery:finish` | Complete current branch |
| `/gitmastery:release` | Create versioned release |
| `/gitmastery:changelog` | Generate Keep a Changelog format |
| `/gitmastery:init` | Initialize git-flow |

### branch-guardian

Enforces git-flow branch protection. Blocks direct commits to main/develop.

### docker-mastery

Docker best practices: optimized Dockerfiles, multi-stage builds, compose configurations.

## Installation

Add the marketplace:

```bash
/plugin marketplace add jugrajsingh/skillgarden
```

Install a plugin:

```bash
/plugin install gitmastery@skillgarden
```

Verify it's working:

```bash
/help
# Should see: /gitmastery:commit, /gitmastery:feature, etc.
```

## Quick Start

After installing gitmastery, just use git normally. The hooks will guide you:

```bash
# This gets blocked with helpful message:
git add .
# → "Git Add Blocked: '.' (current directory) not allowed. List files explicitly."

# This works:
git add src/auth.py src/utils.py

# This gets blocked:
git commit -m "fixed bug"
# → "Git Commit Blocked: Not conventional format. Use: type(scope): subject"

# This works:
git commit -m "fix(auth): handle null token gracefully"
```

Or use the guided workflow:

```bash
/gitmastery:commit
# → Analyzes changes, groups logically, presents each commit for approval
```

## Philosophy

- **Enforce, don't suggest** - Hooks block bad patterns before they happen
- **Guide, don't lecture** - Clear error messages with the fix
- **Compose, don't monolith** - Small plugins that do one thing well
- **Convention over configuration** - Sensible defaults that just work

## Contributing

Want to add a plugin? See [CONTRIBUTING.md](CONTRIBUTING.md) for:

- Git-flow workflow setup
- Plugin structure requirements
- Pre-commit hook configuration

Skills live in `plugins/<name>/skills/`. Hooks live in `plugins/<name>/hooks/`.

## Updating

```bash
/plugin update gitmastery@skillgarden
```

Or update all:

```bash
/plugin marketplace update skillgarden
```

## License

MIT License - see LICENSE file for details.

## Support

- **Issues**: <https://github.com/jugrajsingh/skillgarden/issues>
- **Author**: Jugraj Singh (<jugrajskhalsa@gmail.com>)

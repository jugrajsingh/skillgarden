# SkillGarden

A plugin marketplace for Claude Code that brings developer best practices as composable plugins. Install what you need, they work together seamlessly.

## Available Plugins

### gitmastery

Git workflow validation with enforcement. Explicit file staging, conventional commits, no AI footers.

**What it enforces:**

- `git add .` → Blocked. List files explicitly.
- `git commit -m "fixed stuff"` → Blocked. Use `type(scope): subject`
- AI footers → Blocked automatically

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

Git-flow branch protection. Blocks direct commits to main/develop.

### docker-mastery

Docker best practices: optimized Dockerfiles, multi-stage builds, compose configurations.

*More plugins coming soon.*

## Installation

Add the marketplace:

```bash
/plugin marketplace add jugrajsingh/skillgarden
```

Install plugins you need:

```bash
/plugin install gitmastery@skillgarden
/plugin install docker-mastery@skillgarden
```

Verify installation:

```bash
/help
# Should see plugin commands listed
```

## Quick Start

After installing gitmastery, just work normally:

```bash
# This gets blocked:
git add .
# → "List files explicitly."

# This works:
git add src/auth.py src/utils.py

# Or use the guided workflow:
/gitmastery:commit
# → Analyzes changes, groups logically, presents each commit for approval
```

## Philosophy

- **Enforce, don't suggest** - Block bad patterns before they happen
- **Guide, don't lecture** - Clear error messages with the fix
- **Compose, don't monolith** - Small plugins that do one thing well

## Contributing

Want to add a plugin? See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

## Updating

```bash
/plugin update gitmastery@skillgarden
```

Or update all:

```bash
/plugin marketplace update skillgarden
```

## Support

- **Issues**: <https://github.com/jugrajsingh/skillgarden/issues>
- **Author**: Jugraj Singh (<jugrajskhalsa@gmail.com>)

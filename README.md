# SkillGarden

**Multi-plugin marketplace for Claude Code skills and tools.**

SkillGarden is a collection of Claude Code plugins for skills and tools I use in day-to-day development. This repository follows git-flow workflow with branch protection enforced via pre-commit hooks.

## Plugins

| Plugin | Description | Status |
|--------|-------------|--------|
| `branch-guardian` | Enforces git-flow branch protection via hooks | Planned |
| `docker-mastery` | Docker best practices, Dockerfiles, compose | Planned |

## Branch Protection

This marketplace enforces git-flow workflow rules:

| Branch | Direct Commits | Allowed Actions |
|--------|----------------|-----------------|
| `main` | Blocked | Release merges, hotfix merges |
| `develop` | Blocked | Feature merges, release starts |
| `feature/*` | Allowed | All development work |
| `release/*` | Allowed | Version bumps, release fixes |
| `hotfix/*` | Allowed | Critical production fixes |

## Installation

Add plugins to your Claude Code configuration:

```json
{
  "plugins": [
    { "source": "path/to/skillgarden/plugins/branch-guardian" },
    { "source": "path/to/skillgarden/plugins/docker-mastery" }
  ]
}
```

## Project Structure

```text
skillgarden/
├── .claude-plugin/
│   └── marketplace.json          # Central plugin registry
├── plugins/
│   ├── branch-guardian/          # Git-flow enforcement
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   └── hooks/
│   └── docker-mastery/           # Docker best practices
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── commands/
│       └── skills/
└── README.md
```

## Git Workflow

This project uses [git-flow-next](https://git-flow.sh/). All development follows:

1. Start feature: `git flow feature start <name>`
2. Commit changes on feature branch
3. Finish feature: `git flow finish`
4. Push: `git push origin develop`

## Commit Rules

- **Conventional commits**: `<type>(<scope>): <subject>`
- **Explicit file paths**: No `git add .` or wildcards
- **No AI footers**: Commits must not include Co-Authored-By: Claude

## Development

```bash
# Initialize git-flow
git flow init --defaults

# Start working on a feature
git flow feature start my-feature

# When done
git flow finish
```

## License

MIT

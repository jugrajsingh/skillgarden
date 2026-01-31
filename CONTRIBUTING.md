# Contributing to SkillGarden

## Prerequisites

- [git-flow-next](https://git-flow.sh/) installed
- [pre-commit](https://pre-commit.com/) installed

## Setup

```bash
# Clone and install pre-commit hooks
git clone git@github.com:jugrajsingh/skillgarden.git
cd skillgarden
pre-commit install --install-hooks
```

## Development Workflow

1. Start feature: `git flow feature start <name>`
2. Make changes and commit (hooks run automatically)
3. Finish feature: `git flow finish`
4. Push: `git push origin develop`

## Commit Rules

- Conventional commits: `<type>(<scope>): <subject>`
- Explicit file paths: No `git add .` or wildcards

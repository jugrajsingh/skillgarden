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

### claudemd

CLAUDE.md lifecycle management. Generate, audit, sync, and optimize hierarchical context files throughout a repository.

**Commands:**

| Command | Description |
|---------|-------------|
| `/claudemd:init` | Generate root + module-level CLAUDE.md files |
| `/claudemd:audit` | Health check all context files for anti-patterns and staleness |
| `/claudemd:sync` | Detect and fix drift between docs and codebase |
| `/claudemd:optimize` | Reduce context cost while preserving signal |

### unstuck

Structured error escalation protocol. 3-strike workflow when stuck on a problem: diagnose, pivot, escalate.

**Commands:**

| Command | Description |
|---------|-------------|
| `/unstuck` | Start the escalation protocol |

### planner

Design brainstorming, implementation planning with 3-file persistence, session recovery, and worktree isolation. Drives the front of the development workflow.

**Commands:**

| Command | Description |
|---------|-------------|
| `/planner:brainstorm` | Explore design ideas through guided dialogue |
| `/planner:plan` | Create implementation plan with task decomposition and batching |
| `/planner:resume` | Recover session state via 5-Question Reboot Test |
| `/planner:handoff` | Generate session transfer document |
| `/planner:worktree` | Set up git worktree isolation for a branch |

**Persistence:** Creates `docs/plans/{slug}-task_plan.md`, `findings.md`, and `progress.md` for cross-session project memory.

### researcher

Parallel sub-agent research with persistent reports. Dispatches locator, analyzer, and pattern-finder agents for evidence-backed codebase analysis.

**Commands:**

| Command | Description |
|---------|-------------|
| `/researcher:research` | Research a codebase question with parallel sub-agents |
| `/researcher:dispatch` | Dispatch parallel agents for independent problems |

**Agents:** locator (haiku, fast file finding), analyzer (sonnet, data flow tracing), pattern-finder (sonnet, existing pattern discovery).

### tidyup

Codebase cleanup and hygiene. Assess dead code, duplication, and staleness, then execute cleanup with safety gates.

**Commands:**

| Command | Description |
|---------|-------------|
| `/tidyup:assess` | Analyze codebase for cleanup candidates (read-only) |
| `/tidyup:cleanup` | Execute cleanup with user approval and test verification |

**Safety:** Never deletes files -- archives to `.archive/` instead. Always runs tests after changes.

### shipit

Batch execution with subagent pipeline, TDD enforcement, code review, verification, and branch completion. The execution engine for plans created by planner.

**Commands:**

| Command | Description |
|---------|-------------|
| `/shipit:execute` | Execute plan with implement-review-verify pipeline |
| `/shipit:tdd` | Run RED-GREEN-REFACTOR cycle for a single task |
| `/shipit:review` | Dispatch comprehensive code review |
| `/shipit:verify` | Evidence-before-claims verification gate |
| `/shipit:ship` | Complete branch (merge, PR, keep, or discard) |
| `/shipit:describe-pr` | Generate PR description from changes and plan |

**Pipeline:** Each task goes through implementer → spec-reviewer → quality-reviewer agents. Uses Claude Code native Tasks for real-time coordination.

### pysmith

Python project scaffolding and best practices. Generate pyproject.toml, Pydantic Settings, pre-commit hooks, and audit existing projects.

**Commands:**

| Command | Description |
|---------|-------------|
| `/pysmith:setup` | Full Python dev environment (pyproject + settings + pre-commit + makefile) |
| `/pysmith:pyproject` | Generate pyproject.toml with uv-native config |
| `/pysmith:settings` | Generate Pydantic Settings + YAML configuration |
| `/pysmith:precommit` | Generate .pre-commit-config.yaml with security hooks |
| `/pysmith:patterns` | Browse 9 copy-paste Python code patterns |
| `/pysmith:audit` | Audit project against Python best practices |

### makesmith

Makefile generation for development and deployment. Supports role-separated Makefiles with self-documenting targets.

**Commands:**

| Command | Description |
|---------|-------------|
| `/makesmith:local` | Generate Makefile.local with dev targets (venv, test, lint) |
| `/makesmith:deploy` | Generate Makefile.deploy with DevOps targets (build, push, deploy) |
| `/makesmith:makefile` | Generate root Makefile that delegates to local/deploy |
| `/makesmith:audit` | Audit Makefiles against conventions |
| `/makesmith:precommit` | Generate mbake pre-commit hook |

### dockercraft

Docker best practices with language-aware generation. Supports Python, Node.js, Go, Rust, Java with multi-stage builds, compose orchestration, and security auditing.

**Commands:**

| Command | Description |
|---------|-------------|
| `/dockercraft:setup` | Full Docker environment (Dockerfile + compose + services) |
| `/dockercraft:dockerfile` | Generate optimized Dockerfile with language detection |
| `/dockercraft:compose` | Generate docker-compose.yml with service detection |
| `/dockercraft:audit` | Audit Dockerfile and compose against security checklist |
| `/dockercraft:optimize` | Analyze and optimize Docker image size |
| `/dockercraft:precommit` | Generate hadolint pre-commit hook |

**Agent:** dockerfile-reviewer (sonnet, security + performance review with severity grading).

### branch-guardian

Git-flow branch protection. Blocks direct commits to main/develop.

## Cross-Plugin Workflows

### Planning and Execution

```text
Idea -> /planner:brainstorm       -> design doc
     -> /planner:plan             -> task plan + persistence files
     -> /researcher:research      -> evidence-backed analysis (optional)
     -> /shipit:execute           -> batch execution with review pipeline
     -> /shipit:verify            -> evidence gate
     -> /shipit:review            -> comprehensive code review
     -> /shipit:ship              -> merge, PR, keep, or discard
```

### Python Project Setup

```text
/pysmith:setup
  -> generates pyproject.toml, config/settings.py, .pre-commit-config.yaml
  -> delegates to /makesmith:local for Makefile.local
  -> runs make -f Makefile.local setup-local

/dockercraft:setup
  -> generates Dockerfile, .dockerignore
  -> generates docker-compose.yml
  -> optionally starts services

/makesmith:deploy
  -> generates Makefile.deploy with Docker build/push/deploy
  -> references Dockerfile built by dockercraft
```

Session recovery: `/planner:resume` reads persistence files and rebuilds context.
Session transfer: `/planner:handoff` generates a document for the next session.
Maintenance: `/tidyup:cleanup` assesses and removes dead code with safety gates.

## Installation

Add the marketplace:

```bash
/plugin marketplace add jugrajsingh/skillgarden
```

Install plugins you need:

```bash
/plugin install gitmastery@skillgarden
/plugin install claudemd@skillgarden
/plugin install unstuck@skillgarden
/plugin install planner@skillgarden
/plugin install researcher@skillgarden
/plugin install tidyup@skillgarden
/plugin install shipit@skillgarden
/plugin install pysmith@skillgarden
/plugin install makesmith@skillgarden
/plugin install dockercraft@skillgarden
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
- **Persist, don't forget** - 3-file persistence for cross-session memory
- **Evidence, don't claim** - file:line references and test proof required

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

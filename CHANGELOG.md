# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-02-01

### Added

- pysmith plugin for Python project scaffolding and best practices auditing
  - Skills: setup, pyproject, settings, precommit, patterns, audit
  - 9 copy-paste code patterns (repository, service layer, middleware, caching, retry, rate limiter, error handling, background task, DI)
  - Pre-commit base config reference for standardizing project setup
- makesmith plugin for Makefile generation and auditing
  - Skills: local, deploy, makefile, audit, precommit
  - Role-separated Makefiles (Makefile.local, Makefile.deploy, root Makefile)
  - Multi-registry tag-on-push pattern, per-pipeline deployment
- dockercraft plugin for Docker best practices and optimization
  - Skills: setup, dockerfile, compose, audit, optimize, precommit
  - Language references: Python, Node.js, Go, Rust, Java, multi-language
  - dockerfile-reviewer agent (sonnet) for security/performance review
- planner plugin for design brainstorming and implementation planning
  - Skills: brainstorm, plan, resume, handoff, worktree
  - 3-file persistence for cross-session memory
- researcher plugin for parallel sub-agent codebase research
  - Skills: research, dispatch
  - Agents: locator (haiku), analyzer (sonnet), pattern-finder (sonnet)
- shipit plugin for batch execution with subagent pipeline
  - Skills: execute, tdd, review, verify, ship, describe-pr
  - Agents: implementer, code-reviewer, spec-reviewer, quality-reviewer
- tidyup plugin for codebase cleanup and hygiene
  - Skills: assess, cleanup
  - Safety: archives to .archive/ instead of deleting
- no-commit-to-branch pre-commit hook protecting main and develop

### Changed

- Replaced docker-mastery marketplace entry with dockercraft
- Updated marketplace version to 0.3.0
- Updated README with cross-plugin setup workflow

## [0.2.0] - 2026-01-31

### Added

- claudemd plugin for CLAUDE.md lifecycle management (init, audit, sync, optimize)
- unstuck plugin for structured error escalation protocol (diagnose, pivot, escalate)

### Fixed

- Gitmastery commit hook rejecting HEREDOC and multiline commit messages
- Gitmastery commit hook rejecting breaking change `!` indicator

## [0.1.0] - 2026-01-31

### Added

- Marketplace structure and best practices for plugin development
- Gitmastery plugin with git workflow validation hooks
  - PreToolUse hooks for git add/commit validation
  - Skills: commit, feature, finish, release, init, changelog
  - Blocks wildcards, enforces conventional commits, no AI footers
- Plugin development gotchas documentation in CLAUDE.md

### Changed

- Refactored documentation structure

### Fixed

- Marketplace schema to use correct metadata field per official docs

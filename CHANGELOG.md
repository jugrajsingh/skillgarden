# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - 2026-02-07

### Added

- skillforge plugin for skill design best practices
  - Audit existing skills against structure, modularization, and gotcha checklist
  - Create new skills with reference file patterns and token-aware architecture

### Changed

- Move allowed-tools from commands to skills across all plugins (canonical placement)
- Enhance gitmastery commit skill with critical rules, anti-patterns, and AI footer prohibition
- Add SKIP env var for merge commits in gitmastery finish/release workflows
- Modularize makesmith skills into reference files (auditing, generating-deploy, generating-local)
- Modularize dockercraft generating-compose into 9 service-specific reference files
- Update Python Dockerfile reference for dockercraft
- Bump plugin versions: gitmastery 0.2.0, makesmith 0.2.0, dockercraft 0.2.0, claudemd/planner/researcher/shipit/tidyup/unstuck 0.1.1

## [0.5.0] - 2026-02-02

### Added

- grepai embedder-config skill for viewing, changing, and troubleshooting embedding provider/model configuration
  - Supports Ollama, OpenAI, and LM Studio providers
  - Handles cascading changes (dimensions, re-indexing, workspace propagation)
  - Troubleshooting checks for connectivity, model availability, dimension mismatch
- grepai mcp-setup skill for IDE-agnostic MCP server configuration
  - Supports Claude Code, Cursor, Windsurf, and generic .mcp.json
  - Scope selection (project, user global, project-specific)
  - Workspace mode with --workspace flag for cross-project search

### Changed

- grepai checking-status skill detects services by image ancestry instead of hardcoded container names
- grepai initializing skill uses non-interactive `grepai init --yes` with provider/backend flags
- grepai initializing skill adds CLAUDE.md workspace guidance when in workspace mode
- grepai setting-up skill delegates MCP registration to new mcp-setup skill
- grepai workspace-managing skill uses piped input for non-interactive workspace creation
- grepai workspace-managing skill uses absolute paths and documents project name derivation
- Docker Compose switched from GOB to Qdrant backend with bge-m3 embedding model
- grepai plugin version bumped to 0.3.0
- Marketplace version bumped to 0.5.0

## [0.4.0] - 2026-02-01

### Added

- grepai plugin for semantic code search setup, initialization, and health monitoring
  - Commands: /grepai:setup, /grepai:init, /grepai:status
  - Skills: setting-up (9-step guided orchestrator), initializing (config generation), checking-status (health diagnostics)
  - Docker Compose template with Ollama for embeddings
  - Embedding provider selection (Ollama/OpenAI) with model choices
  - Storage backend selection (GOB default, PostgreSQL optional)
  - MCP server registration (global or project scope)
- Root docker-compose.yml for grepai Ollama infrastructure
- Inspiration submodules for grepai-skills and superpowers-agent-skills

### Fixed

- grepai plugin defaults to GOB storage instead of PostgreSQL due to pgvector UTF-8 chunking bug (yoanbernabeu/grepai#96)

### Changed

- grepai plugin defaults to nomic-embed-text (768 dims, 274MB) over mxbai-embed-large for faster setup

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

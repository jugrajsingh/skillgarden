# Changelog

All notable changes to the **gitmastery** plugin.

## [0.4.1] - 2026-03-26

### Added

- 4-tier pre-commit failure handling in committing skill (hook self-fix, CLI autofix, agent edits, user escalation)
- `Bash(ruff *)` to committing skill allowed-tools for autofix CLI
- mypy stash conflict guidance and fix pattern

## [0.4.0] - 2026-02-25

### Fixed

- Add missing `--add` flag to `git update-index --cacheinfo` for new submodules in committing skill

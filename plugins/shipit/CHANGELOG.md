# Changelog

All notable changes to the **shipit** plugin.

## [0.2.1] - 2026-03-26

### Fixed

- Removed stale `subagent_type: general-purpose` parameter from reviewing-code Task dispatch
- Added TaskCreate and TaskUpdate to executing skill allowed-tools to match actual usage

## [0.2.0] - 2026-02-25

### Added

- codex-review command and codex-reviewing skill for Codex-powered code review via MCP
- .mcp.json to auto-register Codex MCP server with the plugin
- Support for full codebase, diff-based, and file-specific review scopes
- Optional model and reasoning effort overrides
- Follow-up conversation via codex-reply thread continuity

### Changed

- Skill descriptions rewritten to "Use when..." format (all 6 skills)
- Extracted 3-stage pipeline details to `skills/executing/references/pipeline-stages.md`
- Extracted TDD phase procedures to `skills/tdd-cycling/references/phase-details.md`
- Extracted evidence collection to `skills/verifying/references/evidence-collection.md`
- Reduced word counts: executing 1101→651, tdd-cycling 845→402, verifying 862→522

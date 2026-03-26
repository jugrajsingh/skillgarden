# Changelog

All notable changes to the grepai plugin will be documented in this file.

## [0.3.1] - 2026-03-26

### Fixed

- Restored AskUserQuestion to skill allowed-tools (initializing, setting-up)

## [0.3.0] - 2026-02-25

### Changed

- Aligned all 6 skill descriptions to "Use when..." triggering format
- Renamed skill directories to avoid command/skill naming collisions:
  - embedder-config → configuring-embedder
  - mcp-setup → setting-up-mcp
- Updated commands to invoke renamed skills
- Extracted reference files for token efficiency:
  - configuring-embedder: provider-changes.md, reindex.md, troubleshooting.md
  - workspace-managing: create-workflow.md, output-templates.md
  - setting-up: infrastructure-setup.md
  - checking-status: report-format.md
  - initializing: workspace-setup.md
  - setting-up-mcp: mcp-configs.md
- All skills now under 500-word body limit

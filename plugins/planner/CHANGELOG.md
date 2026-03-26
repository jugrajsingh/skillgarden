# Changelog

All notable changes to the planner plugin will be documented in this file.

## [0.2.0] - 2026-03-26

### Added

- Hard-gate in brainstorming preventing implementation before design approval
- Scope decomposition check for multi-subsystem requests
- Spec self-review (placeholder scan, consistency, scope, ambiguity)
- User review gate with explicit approval before proceeding
- Git commit of approved design doc
- Interface Contracts section in design doc template
- Existing codebase awareness guidance

### Changed

- Plan file paths from flat `docs/plans/{SLUG}-*.md` to directory `docs/plans/{SLUG}/*.md`
- Removed 200-line design doc limit — scale depth to complexity
- Design doc status flow: "proposal" → "approved" after gate

## [0.1.1] - 2026-02-25

### Changed

- Aligned all 5 skill descriptions to "Use when..." triggering format
- Extracted reference files for token efficiency:
  - brainstorming: question-flows.md, design-doc-template.md
  - planning: task-format.md
  - resuming: reboot-test.md
  - worktrees: setup-detection.md
- All skills now under 500-word body limit

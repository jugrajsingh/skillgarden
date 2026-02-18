# Changelog

All notable changes to the **claudemd** plugin.

## [Unreleased]

### Changed

- Renamed skills to avoid command/skill naming collision (audit→auditing, init→initializing, optimize→optimizing, sync→syncing)
- Updated all 4 commands to invoke renamed skills
- Skill descriptions rewritten to "Use when..." format
- Extracted reference files for all 4 skills:
  - auditing: `references/audit-checks.md`, `references/report-template.md`
  - initializing: `references/discovery-phase.md`, `references/judgment-phase.md`, `references/generation-phase.md`, `references/report-template.md`
  - optimizing: `references/optimizations.md`, `references/report-templates.md`
  - syncing: `references/drift-analysis.md`, `references/report-templates.md`

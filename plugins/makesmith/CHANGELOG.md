# Changelog

All notable changes to the **makesmith** plugin.

## [0.2.1] - 2026-03-26

### Added

- CLAUDE.md Commands section update step in generating-local and generating-deploy
- Expanded Python audit checks with Makefile integration category

### Changed

- Updated Makefile templates with improved target structure
- Agent-first workflow: CLAUDE.md always updated so agents use Makefile targets

## [0.2.0] - 2026-02-25

### Changed

- Skill descriptions rewritten to "Use when..." format (all 5 skills)
- Extracted universal checks to `skills/auditing/references/universal-checks.md`
- Extracted common makefile template to `skills/generating-deploy/references/common-template.makefile`
- Extracted root makefile template to `skills/generating-makefile/references/root-makefile-template.makefile`
- Reduced skill word counts: auditing 627→377, generating-deploy 1244→453, generating-local 820→445, generating-makefile 546→295, generating-precommit 371→241

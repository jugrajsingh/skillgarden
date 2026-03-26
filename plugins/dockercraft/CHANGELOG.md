# Changelog

All notable changes to the **dockercraft** plugin.

## [0.2.1] - 2026-03-26

### Fixed

- Restored AskUserQuestion to skill allowed-tools (auditing, optimizing, setting-up)

## [0.2.0] - 2026-02-25

### Changed

- Skill descriptions rewritten to "Use when..." format (all 6 skills)
- Extracted audit check tables to `skills/auditing/references/audit-checks.md`
- Extracted compose skeleton to `skills/generating-compose/references/compose-skeleton.yaml`
- Extracted .dockerignore template to `skills/generating-dockerfile/references/dockerignore-template`
- Reduced skill word counts: auditing 547→290, generating-compose 630→459, generating-dockerfile 616→449

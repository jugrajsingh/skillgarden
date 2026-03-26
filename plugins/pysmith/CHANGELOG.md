# Changelog

All notable changes to the **pysmith** plugin.

## [0.1.1] - 2026-03-26

### Added

- Makefile integration as 5th audit category in auditing skill
- YAML discovery with YamlConfigSettingsSource in generating-settings
- CLAUDE.md commands step in setting-up for agent Makefile usage

### Changed

- Expanded settings template and audit checks references

## [0.1.0] - 2026-02-25

### Changed

- Skill descriptions rewritten to "Use when..." format (auditing, generating-precommit, setting-up)
- Extracted audit check tables to `skills/auditing/references/audit-checks.md`
- Extracted pyproject.toml template to `skills/generating-pyproject/references/pyproject-template.toml`
- Extracted settings template to `skills/generating-settings/references/settings-template.py`
- Extracted example env YAML to `skills/generating-settings/references/example-env.yaml`
- Reduced skill word counts: auditing 847→282, generating-pyproject 1583→569, generating-settings 1287→485, setting-up 845→456

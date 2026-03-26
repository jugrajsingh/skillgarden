# Changelog

All notable changes to the **researcher** plugin.

## [0.2.0] - 2026-03-26

### Added

- research-orchestrator agent for autonomous decompose-dispatch-synthesize workflow
- parallel-dispatcher agent for autonomous dispatch-collect-merge workflow

### Changed

- Researching and dispatching skills converted to thin wrappers (skill-wraps-agent pattern)
- Skills handle user interaction only, delegating core logic to agents via Task tool

## [0.1.1] - 2026-02-25

### Changed

- Skill descriptions rewritten to "Use when..." format (dispatching, researching)
- Extracted agent prompt templates to `skills/researching/references/agent-prompts.md`
- Extracted report format to `skills/researching/references/report-format.md`
- Extracted conflict/merge procedures to `skills/dispatching/references/conflict-and-merge.md`
- Reduced word counts: dispatching 698→583, researching 1270→568

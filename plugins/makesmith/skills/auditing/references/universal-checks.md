# Universal Makefile Checks

## Conventions

| Check | Pass Criteria |
|-------|---------------|
| .DEFAULT_GOAL set | `.DEFAULT_GOAL := help` present |
| help target exists | `help:` target with grep/awk pattern |
| Self-documenting | All public targets have `## description` comment |
| .PHONY declarations | All non-file targets listed in .PHONY |
| Private target convention | Internal targets use underscore prefix (_target) or define macros |
| Section separators | Comment blocks separating logical sections |

## Variables

| Check | Pass Criteria |
|-------|---------------|
| No hardcoded paths | Registry URLs, namespaces in variables |
| No hardcoded versions | VERSION derived from git or variable |
| Consistent naming | SCREAMING_SNAKE for variables |
| Overridable where needed | `?=` for KUBE_CONTEXT, NAMESPACE |

## Structure

| Check | Pass Criteria |
|-------|---------------|
| Role separation | Dev targets in Makefile.local, deploy in Makefile.deploy |
| No mixed concerns | Build/push/deploy not mixed with test/lint/format |
| DRY compliance | Repeated docker/helm commands use private targets or define macros |
| Tag-on-push pattern | build-image tags locally, push-image tags for registry |
| Root delegates | Root Makefile delegates to Makefile.local/deploy, no inline commands |

## Best Practices

| Check | Pass Criteria |
|-------|---------------|
| Tab indentation | Recipes use tabs, not spaces |
| No shell assignment in recipe | Use `$(shell ...)` in variables, not in recipes |
| Quiet prefix usage | `@` prefix on echo, not on commands that might fail |
| Error handling | Use `\|\| true` only on intentional ignore |

## Agent Integration

| Check | Pass Criteria |
|-------|---------------|
| CLAUDE.md Commands section | Lists all Makefile targets the agent should use |
| NEVER instruction | CLAUDE.md contains "NEVER run directly" with list of banned raw commands |
| Script targets documented | Project-specific script targets listed in CLAUDE.md |
| Deploy targets documented | If Makefile.deploy exists, deploy commands listed in CLAUDE.md |

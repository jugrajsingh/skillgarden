---
name: auditing
description: Audit Dockerfile and docker-compose.yml against security, performance, and production readiness checklist. Dispatches dockerfile-reviewer agent for detailed analysis.
allowed-tools:
  - Read
  - Glob
  - Grep
  - AskUserQuestion
  - Task
---

# Audit Docker Configuration

Comprehensive audit of Dockerfile and docker-compose.yml against best practices.

## Checks

### Security

| Check | Pass Criteria |
|-------|---------------|
| Non-root USER | USER directive present, not root |
| No secrets in ENV/ARG | No passwords, keys, tokens in ENV or ARG |
| Base image pinned | Specific version tag, not :latest |
| No --privileged | compose services don't use privileged mode |
| .dockerignore exists | Excludes .env, .git, secrets |
| No ADD for remote URLs | COPY preferred over ADD |

### Performance

| Check | Pass Criteria |
|-------|---------------|
| Multi-stage build | Multiple FROM statements |
| Deps before source | COPY lock files before source code |
| Cache mounts used | --mount=type=cache for package managers |
| .dockerignore comprehensive | Excludes node_modules, __pycache__, .git, tests |
| Minimal base image | alpine, slim, or distroless variants |
| Package cache cleaned | apt-get clean or rm -rf /var/lib/apt/lists in same RUN |

### Production Readiness

| Check | Pass Criteria |
|-------|---------------|
| HEALTHCHECK defined | HEALTHCHECK instruction in Dockerfile |
| Exec form CMD | CMD uses JSON array, not shell form |
| PID 1 handling | App is PID 1 or uses tini/dumb-init |
| Restart policy | restart: unless-stopped in compose |
| Resource limits | mem_limit/cpus set in compose |
| Logging to stdout | No file-based logging in CMD |

### Compose Checks

| Check | Pass Criteria |
|-------|---------------|
| Named networks | Custom network, not default bridge |
| Health conditions | depends_on uses condition: service_healthy |
| Named volumes | No anonymous volumes |
| No hardcoded secrets | Environment uses variable references or env_file |
| Service ordering | depends_on with health checks |

## Workflow

### 1. Find Docker Files

```text
Glob: Dockerfile, Dockerfile.*, docker-compose*.yml, docker-compose*.yaml, .dockerignore
```

### 2. Run Checks

For each file found, evaluate all relevant checks.

### 3. Dispatch Reviewer Agent

For detailed Dockerfile analysis, dispatch the dockerfile-reviewer agent:

```text
Task: dockerfile-reviewer agent
Input: Dockerfile path and optional compose path
Output: Structured review with severity levels
```

### 4. Generate Report

Use the audit-report.md template. Fill in:

- Security checks with pass/fail/partial indicators
- Performance checks
- Production readiness checks
- Compose checks (if applicable)
- Findings with file:line references
- Recommendations by priority

### 5. Ask About Fixes

After presenting the report, ask via AskUserQuestion:

- "Fix all issues" - Apply automatic fixes where possible
- "Fix critical only" - Only security and production issues
- "Report only" - No changes

## Priority Classification

| Priority | Criteria |
|----------|----------|
| High | Security: root user, secrets in image, no .dockerignore |
| Medium | Performance: no multi-stage, no cache mounts, large base image |
| Low | Production: missing HEALTHCHECK, shell form CMD, no resource limits |

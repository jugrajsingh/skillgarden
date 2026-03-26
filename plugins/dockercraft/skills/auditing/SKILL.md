---
name: auditing
description: Use when checking Docker configuration for security gaps, performance issues, or production readiness problems in Dockerfile or docker-compose.yml
allowed-tools:
  - Read
  - Glob
  - Grep
  - Task
  - AskUserQuestion
---

# Audit Docker Configuration

Comprehensive audit of Dockerfile and docker-compose.yml against best practices.

## Checks

Read `references/audit-checks.md` for the full checklist. Four categories:

1. **Security** - Non-root USER, no secrets in ENV/ARG, pinned base images, no --privileged, .dockerignore
2. **Performance** - Multi-stage builds, deps before source, cache mounts, minimal base image
3. **Production Readiness** - HEALTHCHECK, exec form CMD, PID 1 handling, restart policy, resource limits
4. **Compose** - Named networks/volumes, health conditions, no hardcoded secrets

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

---
name: auditing
description: Audit Helm chart against security, best practices, and production readiness checklist. Reports findings with severity levels and offers fixes.
allowed-tools:
  - Read
  - Glob
  - Grep
  - AskUserQuestion
---

# Audit Helm Chart

Comprehensive audit of a Helm chart against security, best practices, and production readiness.

## Workflow

### 1. Find Chart Files

```text
Glob: chart/Chart.yaml, chart/values.yaml, chart/templates/*.yaml, chart/templates/*.tpl, chart/templates/*.txt
```

If no chart found, report and exit.

### 2. Read All Chart Files

Read every file in `chart/` to understand the full picture.

### 3. Run Checklist

Read `references/checklist.md` and evaluate each check against the chart files.

### 4. Generate Report

Present findings grouped by category with severity indicators:

```text
Helm Chart Audit: {chart_name}

SECURITY
  [PASS] Non-root user configured
  [FAIL] Capabilities not dropped — add capabilities.drop: [ALL]
  [PASS] No secrets in values.yaml

BEST PRACTICES
  [PASS] Checksum annotations present
  [WARN] Resource limits empty — define actual limits
  [PASS] Labels via _helpers.tpl

PRODUCTION READINESS
  [PASS] Probes configured (exec)
  [FAIL] NodeSelector empty — add node targeting
  [PASS] NOTES.txt customized

Summary: {pass_count} passed, {warn_count} warnings, {fail_count} failures
```

### 5. Ask About Fixes

Present via AskUserQuestion:

| Option | Description |
|--------|-------------|
| Fix all issues | Apply fixes for all FAIL and WARN items |
| Fix critical only | Fix FAIL items only (security and production) |
| Report only | No changes, just the audit report |

### 6. Apply Fixes

For each fixable issue, edit the appropriate file. Report what was changed.

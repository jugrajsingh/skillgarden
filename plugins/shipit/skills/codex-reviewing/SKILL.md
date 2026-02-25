---
name: codex-reviewing
description: Use when code needs review via OpenAI Codex — delegates full or scoped review to Codex MCP, normalizes output into shipit report format
allowed-tools:
  - mcp__codex__codex
  - mcp__codex__codex-reply
  - Read
  - Bash(git diff*)
  - Bash(git log*)
  - Bash(mkdir *)
  - AskUserQuestion
---

# Codex Code Review

Delegate code review to OpenAI Codex via MCP, then normalize output into shipit's standard report format.

## Prerequisites

This skill requires the Codex MCP server. The shipit plugin ships .mcp.json to register it automatically. If the mcp__codex__codex tool is not available:

1. Verify Node.js/npm is installed: node --version
2. Reinstall the shipit plugin to reload .mcp.json
3. Restart Claude Code

## Input

$ARGUMENTS may contain flags and paths:

- --scope full|diff|files (default: full)
- --model MODEL (optional, overrides Codex default)
- --effort low|medium|high|xhigh (optional, overrides Codex default)
- Remaining args are file/directory paths (implies --scope files)

If $ARGUMENTS is empty, ask via AskUserQuestion with options:

- "Full codebase review" (default) — Codex reviews the entire project
- "Changed files only" — review diff against develop/main
- "Specific files/directories" — then ask for paths

## Step 1: Parse Arguments and Determine Scope

Parse $ARGUMENTS for flags. Set defaults:

- scope = "full" unless --scope or paths provided
- model = nil unless --model provided
- effort = nil unless --effort provided
- If bare paths provided without --scope, set scope = "files"

## Step 2: Gather Context

Based on scope:

- full: No diff needed. The cwd is the project root. Codex will explore on its own.

- diff: Run git commands to gather changes:

  ```bash
  git diff develop...HEAD
  git diff develop...HEAD --stat
  ```

  If diff is empty, report "No changes found" and stop.

- files: Validate provided paths exist via Read. Build a file list.

## Step 3: Generate Slug

Derive a slug for the report:

- Start with date prefix: YYYY-MM-DD
- From branch name: feature/add-auth -> add-auth
- Sanitize: lowercase, hyphens only

Example slug: 2026-02-25-add-auth

Write path: docs/reviews/{slug}-codex-review.md

## Step 4: Build Codex MCP Call

Construct the mcp__codex__codex tool call:

prompt: Varies by scope:

- full: "Review this codebase comprehensively. Focus on architecture, correctness, security, performance, and code quality."
- diff: "Review these code changes:\n\n{diff content}\n\nFocus on correctness, security, and quality of the changes."
- files: "Review these specific files: {file list}. Focus on architecture, correctness, security, performance, and quality."

developer-instructions: Always include:

  You are a senior code reviewer. Produce a structured review.

  For each finding:

- Severity: minor, major, or critical
- File and line number (exact)
- Description of the issue
- Suggested fix (if applicable)
- Category: architecture, correctness, security, performance, quality, testing

  End with an overall verdict: APPROVE, REQUEST CHANGES, or COMMENT.
  Group findings by severity (critical first, then major, then minor).

sandbox: "read-only"

approval-policy: "never"

model: Only include if user specified --model.

config: If user specified --effort, include model_reasoning_effort set to the effort value.

Call the tool and capture the response. Store the threadId from the response for potential follow-up.

If the tool call fails or returns an error:

- MCP tool not found: display the Prerequisites section guidance
- Codex authentication error: ask user to verify Codex credentials (run codex --version to check)
- Timeout or no response: inform user the review may be too large, suggest narrowing scope with --scope diff or specific paths

## Step 5: Normalize Output

Parse Codex's free-form response and normalize into shipit report format.

Map severity terms:

- "critical" -> ◆◆
- "major" -> ◆
- "minor" -> ◇

Extract:

- Individual findings with file:line references
- Severity counts
- Overall verdict (APPROVE, REQUEST CHANGES, or COMMENT)

If Codex output cannot be parsed (no clear findings structure), present raw output under a "Raw Review" heading instead.

Critically evaluate Codex's claims. If any finding contradicts your own knowledge, add a note: "Claude note: {disagreement with evidence}".

## Step 6: Write Report

```bash
mkdir -p docs/reviews
```

Write to docs/reviews/{slug}-codex-review.md with this structure:

```text
# Code Review: {slug}

**Reviewer:** Codex (via OpenAI)
**Date:** {YYYY-MM-DD}
**Scope:** {full | diff | files: path1, path2}
**Verdict:** {APPROVE | REQUEST CHANGES | COMMENT}

## Findings

### ◆◆ Critical
- file:line — description
  Suggestion: fix

### ◆ Major
- file:line — description

### ◇ Minor
- file:line — description

## Summary
{normalized summary}
```

Group by severity — omit sections with zero findings.

## Step 7: Present Summary and Offer Follow-Up

Output a summary block:

```text
## Review Summary

Findings: {total}
  Critical: {N}
  Major: {N}
  Minor: {N}

Top Issues:
1. {severity_symbol} {file}:{line} — {description}
2. {severity_symbol} {file}:{line} — {description}
3. {severity_symbol} {file}:{line} — {description}

Full report: docs/reviews/{slug}-codex-review.md
```

Then ask via AskUserQuestion:

- "Ask Codex a follow-up question" — use codex-reply with stored threadId
- "Address issues now" — start fixing from highest severity
- "Acknowledge and continue" — user handles it later

If user chooses follow-up, call mcp__codex__codex-reply with threadId and user's question. Present response and offer same choices again.

## Rules

- Always use read-only sandbox — code review never writes to the project
- Every finding in the report must include a file:line reference
- Review report always written to docs/reviews/ for traceability
- Treat Codex output as peer input — flag disagreements with evidence
- Store threadId for follow-up conversation continuity

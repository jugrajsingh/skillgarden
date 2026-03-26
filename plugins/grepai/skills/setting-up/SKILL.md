---
name: setting-up
description: Use when setting up GrepAI from scratch — Docker, embedding provider, storage backend, MCP registration, and first indexing
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash(docker *)
  - Bash(grepai *)
  - Bash(ollama *)
  - Bash(curl *)
  - Bash(which *)
  - Bash(claude *)
  - Write
  - Edit
  - Skill
  - AskUserQuestion
---

# GrepAI Full Setup

Guided orchestrator for GrepAI semantic code search. Walks through prerequisites, infrastructure, embedding config, storage, MCP integration, and indexing.

## Step 1: Prerequisites Check

### grepai CLI

```bash
which grepai
```

If missing, show install instructions:

```text
Install grepai:

  macOS/Linux:
    brew install grepai/tap/grepai

  Or via curl:
    curl -fsSL https://get.grepai.dev | sh

  Windows (PowerShell):
    irm https://get.grepai.dev/install.ps1 | iex
```

Stop and ask user to install before continuing.

### Docker

```bash
which docker
```

If missing, instruct to install Docker Desktop or Docker Engine and stop.

## Steps 2-5: Storage, Docker, Embedding

Ask storage backend (GOB recommended for single-project, PostgreSQL/Qdrant for workspaces). Set up Docker Compose from plugin templates (`${CLAUDE_PLUGIN_ROOT}/templates/docker-compose-{backend}.yml`). Ask embedding provider (Ollama recommended, OpenAI) and model. Pull model if Ollama.

See references/infrastructure-setup.md for AskUserQuestion prompts, Docker compose templates, model options by provider, and cost estimates.

## Step 6: Initialize grepai

Delegate to the initializing skill with collected choices:

Invoke the `grepai:initializing` skill and follow it exactly.

Pass context: chosen provider, model, storage backend, DSN if postgres, endpoint if qdrant.

**For workspace mode:** tell the initializing skill to use GOB for the local per-project config. The workspace handles its own shared store separately via `~/.grepai/workspace.yaml`.

## Step 7: MCP Registration

Delegate to the `grepai:setting-up-mcp` skill and follow it exactly.

Pass context: workspace name (if workspace mode was chosen), so it can offer the `--workspace` flag option.

## Step 8: Official Skills Plugin

Inform user about the official grepai-skills plugin:

```text
The official grepai-skills plugin provides 27 reference skills for advanced
configuration tuning, troubleshooting, and workflow optimization.

Install via Claude Code plugin marketplace:
  /plugin marketplace add yoanbernabeu/grepai-skills
  /plugin install grepai-complete@grepai-skills

Note: These are reference skills (no /commands). The grepai MCP tools
(grepai_search, grepai_trace_*) handle search and trace natively.
```

## Step 9: Start Indexing

Present via AskUserQuestion:

```text
Start grepai watch daemon now? This monitors file changes and updates the index.

○ Yes, start in background (Recommended)
○ No, I'll start later
```

If yes, branch based on mode:

**Single project:**

```bash
grepai watch --background
```

**Workspace mode:**

```bash
grepai watch --workspace {NAME} --background
```

Both per-project and workspace watchers can coexist. For workspace mode, the workspace watcher is the primary one to start.

## Final Summary

Print configuration summary showing infrastructure, embedding, storage, integration, and workspace details with useful commands. See references/infrastructure-setup.md for the summary template.

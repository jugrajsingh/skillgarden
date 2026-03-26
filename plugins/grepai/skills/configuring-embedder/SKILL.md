---
name: configuring-embedder
description: Use when you need to view, change, or troubleshoot the embedding provider and model for GrepAI
allowed-tools:
  - Read
  - Glob
  - Grep
  - Edit
  - Bash(grepai *)
  - Bash(docker *)
  - Bash(curl *)
  - Bash(ollama *)
  - Bash(python3 *)
  - AskUserQuestion
---

# GrepAI Embedder Configuration

View, change, or troubleshoot the embedding provider and model used by grepai. Handles cascading changes (dimensions, re-indexing, workspace propagation).

## Model Reference

| Model | Provider | Dims | Speed | Quality | Languages |
|-------|----------|------|-------|---------|-----------|
| nomic-embed-text | Ollama | 768 | Fast | Good | English |
| nomic-embed-text-v2-moe | Ollama | 768 | Fast | Better | 100+ langs |
| bge-m3 | Ollama | 1024 | Medium | Excellent | 100+ langs |
| mxbai-embed-large | Ollama | 1024 | Medium | Better | English |
| all-minilm | Ollama | 384 | Very Fast | Basic | English |
| text-embedding-3-small | OpenAI | 1536 | Fast (API) | Good | Multi |
| text-embedding-3-large | OpenAI | 3072 | Fast (API) | Excellent | Multi |

**OpenAI pricing:** text-embedding-3-small ~$0.02/1M tokens, text-embedding-3-large ~$0.13/1M tokens. Typical project (10k lines) costs ~$0.001.

## Workflow

### 1. Detect Current Configuration

Check MCP registration (`claude mcp list`, `.mcp.json`, `~/.claude.json`), local config (`.grepai/config.yaml`), and workspace config (`grepai workspace list`, `~/.grepai/workspace.yaml`).

**Mode detection:**

- MCP has `--workspace {NAME}` → workspace mode, config in `~/.grepai/workspace.yaml`
- `.grepai/config.yaml` exists, no workspace MCP → local mode
- Both exist → workspace for search, local for chunking/ignore

Display: mode, config path, provider, model, dimensions, endpoint.

### 2. Ask: What To Do

Ask via AskUserQuestion:

```text
What would you like to do?

○ Change embedding model (keep same provider)
○ Change embedding provider (e.g. Ollama → OpenAI)
○ View current config (done — already displayed above)
○ Troubleshoot embedding issues
```

If "View current config" — stop here, already displayed.

### 3. Change Model or Provider

Show available models for current provider (use model reference table above), ask user to pick, check availability (Ollama: verify pulled, offer to pull), apply to correct config file (workspace: `~/.grepai/workspace.yaml`, local: `.grepai/config.yaml`).

For provider switch: collect provider-specific settings (endpoint, API key, parallelism for OpenAI, dimension detection for LM Studio).

See references/provider-changes.md for full model selection flows, provider-specific setup commands, and config file templates.

### 4. Re-Index

Embeddings from different models are incompatible — index must be rebuilt. Warn user, ask to re-index now or later. Clear old index (GOB: remove .gob files, Qdrant: delete collection, PostgreSQL: truncate tables), then run `grepai watch`.

See references/reindex.md for backend-specific re-index commands.

### 5. Troubleshoot

If user chose troubleshoot: check provider connectivity, model availability, config consistency (model/endpoint not swapped, dimensions match reference), workspace vs local mismatch. Report with OK/FAIL/WARN indicators.

See references/troubleshooting.md for check commands and diagnostic steps.

### 6. Print Summary

Print before/after comparison (provider, model, dims), config path, mode, and re-index status. If re-index started, show monitor commands. If manual, show re-index commands.

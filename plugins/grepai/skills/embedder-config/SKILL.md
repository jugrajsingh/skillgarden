---
name: embedder-config
description: View, change, or troubleshoot embedding provider and model configuration for grepai.
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

Determine if running in workspace or local mode by checking multiple sources:

**Check MCP registration for workspace flag:**

```bash
claude mcp list 2>/dev/null
```

```text
Glob: .mcp.json
Read: ~/.claude.json  (look for grepai args with --workspace)
```

**Check local config:**

```text
Glob: .grepai/config.yaml
```

If `.grepai/config.yaml` exists, read it and extract embedder section.

**Check workspace config:**

```bash
grepai workspace list 2>/dev/null
```

If workspaces exist, read `~/.grepai/workspace.yaml` for embedder details.

**Determine active mode:**

- If MCP has `--workspace {NAME}` → workspace mode, config is in `~/.grepai/workspace.yaml`
- If `.grepai/config.yaml` exists and no workspace MCP → local mode
- If both exist → workspace takes precedence for search, local for chunking/ignore

Display current config:

```text
Current Embedder Configuration
─────────────────────────────
Mode:       {workspace: NAME | local}
Config:     {~/.grepai/workspace.yaml | .grepai/config.yaml}
Provider:   {ollama | openai | lmstudio}
Model:      {model name}
Dimensions: {dims}
Endpoint:   {endpoint}
```

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

### 3. Change Embedding Model (Same Provider)

#### 3a. Show Available Models

Filter by current provider.

**For Ollama:**

```text
Available Ollama models:

○ nomic-embed-text — 768 dims, fast, English (Recommended default)
○ nomic-embed-text-v2-moe — 768 dims, fast, 100+ languages
○ bge-m3 — 1024 dims, medium speed, excellent quality, 100+ languages
○ mxbai-embed-large — 1024 dims, medium speed, English
```

**For OpenAI:**

```text
Available OpenAI models:

○ text-embedding-3-small — 1536 dims, $0.02/1M tokens (Recommended)
○ text-embedding-3-large — 3072 dims, $0.13/1M tokens, highest quality
```

Ask via AskUserQuestion with options above.

#### 3b. Check Model Availability (Ollama only)

```bash
docker exec {OLLAMA_CONTAINER} ollama list
```

If selected model not pulled:

```text
Model {MODEL} is not pulled yet. Pull it now?

○ Yes — pull model (may take a few minutes)
○ No — skip, I'll pull it later
```

If yes:

```bash
docker exec {OLLAMA_CONTAINER} ollama pull {MODEL}
```

To find the Ollama container:

```bash
docker ps --filter ancestor=ollama/ollama --format "{{.Names}}" | head -1
```

#### 3c. Apply Model Change

Look up new dimensions from the model reference table. Apply to the correct config file.

**Workspace mode** — edit `~/.grepai/workspace.yaml`:

Change the embedder section under the active workspace:

```yaml
embedder:
    model: {NEW_MODEL}
    dimensions: {NEW_DIMS}
```

**Local mode** — edit `.grepai/config.yaml`:

```yaml
embedder:
  model: {NEW_MODEL}
  dimensions: {NEW_DIMS}
```

Proceed to step 5 (re-index).

### 4. Change Embedding Provider

#### 4a. Ask New Provider

```text
Switch to which provider?

○ Ollama (local, free, private)
○ OpenAI (cloud, fast, pay-per-use)
○ LM Studio (local, GUI-based)
```

#### 4b. Collect Provider-Specific Settings

##### Switching to Ollama

- Check Ollama is running:

```bash
curl -s --max-time 5 http://localhost:11434/api/tags
```

- Ask for model (show Ollama models from reference table)
- Set endpoint: `http://localhost:11434`
- Check if model is pulled, offer to pull

##### Switching to OpenAI

- Ask for API key via AskUserQuestion (or check env `$OPENAI_API_KEY`)
- Validate key:

```bash
python3 -c "
import urllib.request, json
req = urllib.request.Request('https://api.openai.com/v1/models',
    headers={'Authorization': 'Bearer {KEY}'})
resp = urllib.request.urlopen(req)
print(f'Status: {resp.status}')
"
```

- Ask for model (show OpenAI models from reference table)
- Ask for parallelism:

```text
OpenAI parallelism (concurrent API requests)?

○ 4 (Recommended default — safe for all tiers)
○ 8 (good for Tier 2+)
○ 16 (good for Tier 3+ or high-volume plans)
```

- Check rate limits to suggest parallelism:

```bash
python3 -c "
import urllib.request, json
data = json.dumps({'input': 'test', 'model': '{MODEL}'}).encode()
req = urllib.request.Request('https://api.openai.com/v1/embeddings', data=data,
    headers={'Authorization': 'Bearer {KEY}', 'Content-Type': 'application/json'})
resp = urllib.request.urlopen(req)
for h in resp.headers:
    if 'ratelimit' in h.lower():
        print(f'{h}: {resp.headers[h]}')
"
```

- Display rate limits and recommend parallelism based on RPM:
  - Under 500 RPM → parallelism 2
  - 500-3000 RPM → parallelism 4-8
  - 3000-10000 RPM → parallelism 8-16
  - Over 10000 RPM → parallelism 16-32

##### Switching to LM Studio

- Check LM Studio is running:

```bash
curl -s --max-time 5 http://127.0.0.1:1234/v1/models
```

- Set endpoint: `http://127.0.0.1:1234`
- Ask for model name (user must know which model is loaded)
- Detect dimensions:

```bash
curl -s http://127.0.0.1:1234/v1/embeddings \
  -d '{"model": "{MODEL}", "input": ["test"]}' | python3 -c "import sys,json; print(len(json.load(sys.stdin)['data'][0]['embedding']))"
```

#### 4c. Apply Provider Change

Update the correct config file with all new fields.

**Workspace mode** — edit `~/.grepai/workspace.yaml`:

```yaml
embedder:
    provider: {NEW_PROVIDER}
    model: {NEW_MODEL}
    endpoint: {NEW_ENDPOINT}
    dimensions: {NEW_DIMS}
    api_key: {KEY}          # OpenAI only
    parallelism: {N}        # OpenAI only, omit for others
```

**Local mode** — edit `.grepai/config.yaml`:

```yaml
embedder:
  provider: {NEW_PROVIDER}
  model: {NEW_MODEL}
  endpoint: {NEW_ENDPOINT}
  dimensions: {NEW_DIMS}
  api_key: {KEY}            # OpenAI only
  parallelism: {N}          # OpenAI only, omit for others
```

Remove fields that don't apply to the new provider (e.g., remove `api_key` when switching to Ollama).

Proceed to step 5 (re-index).

### 5. Re-Index

**CRITICAL:** Embeddings from different models are incompatible. The index must be rebuilt after any model or provider change.

Warn the user:

```text
⚠ Changing the embedding model requires a full re-index.
  Old embeddings are incompatible with the new model.
  This will re-process all files in the project/workspace.
```

Ask via AskUserQuestion:

```text
Re-index now?

○ Yes — clear old index and start re-indexing
○ No — I'll re-index later manually
```

If yes:

**Local mode (GOB backend):**

```bash
rm -rf .grepai/index.gob .grepai/symbols.gob
grepai watch
```

**Workspace mode (Qdrant):**

Delete the old collection and re-index:

```bash
# Find collection name (usually workspace_{NAME})
curl -s http://localhost:6333/collections | python3 -c "import sys,json; [print(c['name']) for c in json.load(sys.stdin)['result']['collections']]"

# Delete the old collection
curl -s -X DELETE http://localhost:6333/collections/workspace_{NAME}

# Re-index
grepai watch --workspace {NAME}
```

**Workspace mode (PostgreSQL):**

```bash
# Truncate the workspace tables (user should confirm)
# Then re-index
grepai watch --workspace {NAME}
```

If no — print the manual re-index commands for later.

### 6. Troubleshoot Embedding Issues

If user chose troubleshoot in step 2:

#### Check 1: Provider connectivity

For Ollama:

```bash
curl -s --max-time 5 http://localhost:11434/api/tags
```

For OpenAI:

```bash
python3 -c "
import urllib.request
req = urllib.request.Request('https://api.openai.com/v1/models',
    headers={'Authorization': 'Bearer {KEY}'})
resp = urllib.request.urlopen(req)
print(f'Status: {resp.status}')
"
```

#### Check 2: Model availability (Ollama)

```bash
docker exec {OLLAMA_CONTAINER} ollama list
```

Verify the configured model appears in the list.

#### Check 3: Config file consistency

Read config file and verify:

- `model` and `endpoint` are not swapped (common mistake during interactive setup)
- `dimensions` matches the model reference table
- `provider` matches the endpoint URL scheme

#### Check 5: Workspace vs local mismatch

If both workspace and local config exist, verify they use the same model/dimensions. Mixed embeddings in the same store cause search quality issues.

Report all findings with OK/FAIL/WARN indicators and specific fix suggestions.

### 7. Print Summary

```text
============================================================================
Embedder Configuration Updated
============================================================================

Before: {OLD_PROVIDER} / {OLD_MODEL} ({OLD_DIMS} dims)
After:  {NEW_PROVIDER} / {NEW_MODEL} ({NEW_DIMS} dims)

Config:     {config file path}
Mode:       {workspace: NAME | local}
Re-index:   {Required — started | Required — manual | Not needed}

{IF RE-INDEX STARTED}
Re-indexing in progress. Monitor with:
  grepai watch --workspace {NAME} --status   # workspace
  grepai watch --status                      # local
{END IF}

{IF RE-INDEX MANUAL}
Run these commands to re-index:
  {COMMANDS}
{END IF}
============================================================================
```

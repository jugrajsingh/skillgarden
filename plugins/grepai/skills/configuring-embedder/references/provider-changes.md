# Provider Changes — Model Selection and Setup Commands

## Change Model (Same Provider)

### Show Available Models

Filter by current provider from the model reference table in the main skill.

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

### Check Model Availability (Ollama only)

```bash
docker exec {OLLAMA_CONTAINER} ollama list
```

If selected model not pulled, offer to pull:

```bash
docker exec {OLLAMA_CONTAINER} ollama pull {MODEL}
```

Find the Ollama container:

```bash
docker ps --filter ancestor=ollama/ollama --format "{{.Names}}" | head -1
```

### Apply Model Change

Look up new dimensions from the model reference table. Apply to the correct config file.

**Workspace mode** — edit `~/.grepai/workspace.yaml`:

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

## Change Provider

### Ask New Provider

```text
Switch to which provider?

○ Ollama (local, free, private)
○ OpenAI (cloud, fast, pay-per-use)
○ LM Studio (local, GUI-based)
```

### Switching to Ollama

- Check running: `curl -s --max-time 5 http://localhost:11434/api/tags`
- Ask for model (show Ollama models from reference table)
- Set endpoint: `http://localhost:11434`
- Check if model is pulled, offer to pull

### Switching to OpenAI

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

- Ask for model (show OpenAI models)
- Ask for parallelism:

```text
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

- RPM-based recommendations: <500 → 2, 500-3000 → 4-8, 3000-10000 → 8-16, >10000 → 16-32

### Switching to LM Studio

- Check running: `curl -s --max-time 5 http://127.0.0.1:1234/v1/models`
- Set endpoint: `http://127.0.0.1:1234`
- Ask for model name (user must know which model is loaded)
- Detect dimensions:

```bash
curl -s http://127.0.0.1:1234/v1/embeddings \
  -d '{"model": "{MODEL}", "input": ["test"]}' | python3 -c "import sys,json; print(len(json.load(sys.stdin)['data'][0]['embedding']))"
```

### Apply Provider Change Config Template

**Workspace mode** — `~/.grepai/workspace.yaml`:

```yaml
embedder:
    provider: {NEW_PROVIDER}
    model: {NEW_MODEL}
    endpoint: {NEW_ENDPOINT}
    dimensions: {NEW_DIMS}
    api_key: {KEY}          # OpenAI only
    parallelism: {N}        # OpenAI only, omit for others
```

**Local mode** — `.grepai/config.yaml`:

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

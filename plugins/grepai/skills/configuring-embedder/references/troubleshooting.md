# Troubleshooting Embedding Issues

## Check 1: Provider Connectivity

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

## Check 2: Model Availability (Ollama)

```bash
docker exec {OLLAMA_CONTAINER} ollama list
```

Verify the configured model appears in the list.

## Check 3: Config File Consistency

Read config file and verify:

- `model` and `endpoint` are not swapped (common mistake during interactive setup)
- `dimensions` matches the model reference table
- `provider` matches the endpoint URL scheme

## Check 4: Workspace vs Local Mismatch

If both workspace and local config exist, verify they use the same model/dimensions. Mixed embeddings in the same store cause search quality issues.

## Reporting

Report all findings with OK/FAIL/WARN indicators and specific fix suggestions.

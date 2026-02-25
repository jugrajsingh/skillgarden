# Re-Index After Embedder Change

**CRITICAL:** Embeddings from different models are incompatible. The index must be rebuilt after any model or provider change.

Warn the user:

```text
Warning: Changing the embedding model requires a full re-index.
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

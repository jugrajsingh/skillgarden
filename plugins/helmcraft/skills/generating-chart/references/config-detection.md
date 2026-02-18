# Config Pattern Detection

Scan project files to auto-populate configmap/secrets keys.

## Settings Detection

```text
Glob: config/settings.py, config/settings.yaml, src/**/settings.py
```

For Python (Pydantic Settings):

- Extract nested model classes (AWSSettings, SQSSettings, etc.)
- Map to env vars with `__` delimiter: `AWS__AWS_REGION`, `SQS__INPUT_QUEUE`
- Separate sensitive fields (passwords, keys, tokens) -> secrets
- Non-sensitive fields -> configmap

## Language and Probe Detection

```text
Glob: Dockerfile, pyproject.toml, package.json, go.mod
```

- Detect language for probe commands
- Detect ENTRYPOINT for exec probe command (e.g., `pgrep -f main.py`)

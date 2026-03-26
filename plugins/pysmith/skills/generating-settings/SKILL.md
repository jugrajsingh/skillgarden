---
name: generating-settings
description: Generate Pydantic Settings configuration with YAML support. Creates config/settings.py and example.env.yaml for type-safe configuration management. Use when setting up application configuration, adding environment-specific settings, or migrating from os.getenv() to Pydantic Settings.
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash(uv add *)
  - AskUserQuestion
---

# Generate Pydantic Settings Configuration

Create type-safe configuration management with Pydantic Settings and YAML support.

## Philosophy

- **Never use `os.getenv()` in app code** - Use Pydantic Settings
- **Priority: ENV vars > YAML file > defaults** - Flexible override chain
- **Type-safe configuration** - Pydantic validation at startup
- **Nested configuration** - Group related settings (postgres, aws, etc.)
- **Git-friendly** - Commit `example.env.yaml`, gitignore `*.env.yaml`

## Workflow

### 1. Check Existing Files

```text
Glob: config/settings.py, *settings*.py, example.env.yaml, *.env.yaml
```

If settings exist, ask via AskUserQuestion:

- "Merge sections" - Add new sections to existing config
- "Overwrite" - Replace entirely
- "Skip" - Don't modify

### 2. Ask Which Sections to Include

Present multi-select via AskUserQuestion:

```text
Which config sections do you need?

☐ postgres (PostgresSettings) - Database connection
☐ redis (RedisSettings) - Cache/queue connection
☐ aws (AWSSettings) - AWS region, endpoint URL
☐ elasticsearch (ElasticsearchSettings) - Search cluster
☐ sentry (SentrySettings) - Error monitoring
☐ logging (LoggingSettings) - Log level, format
☐ api (APISettings) - Host, port, CORS
```

### 3. Generate config/settings.py

Read `references/settings-template.py` as the base template. Customize:

- Include only user-selected section classes (remove unused BaseModel subclasses)
- Keep the Settings class with only selected sections as fields
- Keep the `get_settings()` cached singleton and convenience export

### 4. Generate example.env.yaml

Read `references/example-env.yaml` as the base template. Customize:

- Include only sections matching user-selected settings
- Remove sections for unselected settings classes

### 5. Update .gitignore

Append if not present:

```gitignore
# Local configuration (secrets)
*.env.yaml
!example.env.yaml
local.*.yaml
```

### 6. Add Dependency

If not already present in pyproject.toml:

```bash
uv add "pydantic-settings[yaml]>=2.0"
```

### 7. Report

```text
Created Pydantic Settings configuration:

config/settings.py
  - Settings class with selected sections
  - Type-safe configuration with validation
  - Cached singleton via get_settings()

example.env.yaml
  - Template with all settings documented
  - Copy to local.env.yaml for local development

.gitignore updated
  - *.env.yaml ignored (except example)

Dependency added:
  - pydantic-settings[yaml]>=2.0

Usage:
  from config.settings import settings

  db_host = settings.postgres.host
  aws_region = settings.aws.aws_region

Next steps:
  1. cp example.env.yaml local.env.yaml
  2. Edit local.env.yaml with your values
  3. Import settings in your code
```

## ENV Variable Mapping

| YAML Path | Environment Variable |
|-----------|---------------------|
| `postgres.host` | `POSTGRES__HOST` |
| `postgres.password` | `POSTGRES__PASSWORD` |
| `aws.aws_region` | `AWS__AWS_REGION` |
| `elasticsearch.hosts` | `ELASTICSEARCH__HOSTS='["http://es:9200"]'` |
| `logging.level` | `LOGGING__LEVEL` |

## YAML Discovery & Runtime Override

The template uses **discoverable YAML files** with `YamlConfigSettingsSource`:

```python
YAML_CONFIG_FILES = ["env.yaml", "local.env.yaml"]
```

- Files are checked in order — **last existing file wins**
- Missing files are **silently skipped** (no errors)
- `env.yaml` = base config (deployed via ConfigMap/secret in k8s)
- `local.env.yaml` = local dev overrides (gitignored, highest priority)

**Runtime override** for scripts that need a different environment:

```python
# In a script (e.g., reset_job.py, reindex_job.py):
settings = Settings(yaml_file="production.env.yaml")
```

The `yaml_file` init kwarg replaces the entire discovery list with a single file.
The underscore prefix avoids collision with the `model_config.yaml_file` key.

This is implemented via `settings_customise_sources()` which pops `yaml_file`
from `init_kwargs` before Pydantic processes them.

## Best Practices

1. **Never commit secrets** - Only `example.env.yaml` goes in git
2. **Use ENV vars in production** - More secure than files
3. **Validate early** - Settings load at import time
4. **Type hints everywhere** - Pydantic validates types
5. **Document sections** - Help future developers
6. **YAML discovery order matters** - Last existing file wins (least specific first)
7. **Use `yaml_file` for scripts** - Don't hardcode production configs

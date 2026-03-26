# Workspace Output Templates

## List Output

```text
============================================================================
GrepAI Workspaces
============================================================================

  {NAME}    backend: {TYPE}    projects: {COUNT}
  {NAME}    backend: {TYPE}    projects: {COUNT}

Manage:
  /grepai:workspace:show {NAME}     View details
  /grepai:workspace:create {NAME}   Create new
============================================================================
```

## Show Output

```text
============================================================================
Workspace: {NAME}
============================================================================

Backend:   {TYPE}
Embedder:  {PROVIDER} / {MODEL}

Projects:
  {PROJECT_1}    {PATH_1}
  {PROJECT_2}    {PATH_2}

Commands:
  /grepai:workspace:add {NAME} /path     Add project
  /grepai:workspace:remove {NAME} proj   Remove project
  /grepai:workspace:status {NAME}        Check index health
============================================================================
```

## Status Output

```text
============================================================================
Workspace Status: {NAME}
============================================================================

Backend:  {TYPE} — {STATUS}

Projects:
  {S} {PROJECT_1}    {FILES} files, {CHUNKS} chunks    last: {TIMESTAMP}
  {S} {PROJECT_2}    {FILES} files, {CHUNKS} chunks    last: {TIMESTAMP}

Watcher:  {RUNNING|STOPPED}

============================================================================
```

Where {S} is one of: OK for indexed, FAIL for failed, STALE for stale/partial.

---
name: setting-up
description: Orchestrate complete Docker environment setup by generating Dockerfile, .dockerignore, and docker-compose.yml, then optionally starting services.
allowed-tools:
  - Read
  - Glob
  - Bash(docker *)
  - AskUserQuestion
  - Skill
---

# Docker Environment Setup (Orchestrator)

Orchestrates Docker-based local development setup.

## What Gets Set Up

1. **Dockerfile** - Multi-stage build with language detection
2. **.dockerignore** - Optimized exclusions
3. **docker-compose.yml** - App + services

## Workflow

### 1. Check Existing Files

```text
Glob: Dockerfile, .dockerignore, docker-compose.yml, docker-compose.yaml
```

Report what exists vs what will be created.

### 2. Generate Dockerfile

**If no Dockerfile:**

Invoke the `dockercraft:generating-dockerfile` skill and follow it exactly.

This:

- Detects project language
- Generates multi-stage Dockerfile
- Creates .dockerignore

### 3. Generate docker-compose.yml

**If no docker-compose.yml:**

Invoke the `dockercraft:generating-compose` skill and follow it exactly.

This:

- Detects required services from dependencies
- Configures health checks
- Sets up volumes and networks

### 4. Ask About Starting Services

Present via AskUserQuestion:

```text
Docker configuration created. Start services now?

○ Yes, start all services (docker compose up -d)
○ No, I'll start them manually later
```

### 5. Start Services (if requested)

```bash
docker compose up -d
```

Wait for services to be healthy:

```bash
docker compose ps
```

### 6. Report Success

```text
============================================================================
Docker Environment Ready
============================================================================

Files created:
  ✓ Dockerfile         - Multi-stage build
  ✓ .dockerignore      - Optimized exclusions
  ✓ docker-compose.yml - App + {n} services

Services running:
  ✓ app        - http://localhost:{port}
  ✓ postgres   - localhost:5432
  ✓ redis      - localhost:6379

Commands:
  docker compose up -d      # Start services
  docker compose logs -f    # View logs
  docker compose down       # Stop services
  docker compose build      # Rebuild image

Development workflow:
  1. Make code changes
  2. docker compose restart app  # Restart to pick up changes

For hot reload, mount source in docker-compose.yml (already configured)
============================================================================
```

## Integration

This skill complements pysmith:setting-up:

1. Run pysmith:setup for native Python development
2. Run dockercraft:setup for containerized development

Both can coexist.

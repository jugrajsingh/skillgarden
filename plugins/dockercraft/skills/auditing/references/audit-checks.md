# Docker Audit Checks

## Security

| Check | Pass Criteria |
|-------|---------------|
| Non-root USER | USER directive present, not root |
| No secrets in ENV/ARG | No passwords, keys, tokens in ENV or ARG |
| Base image pinned | Specific version tag, not :latest |
| No --privileged | compose services don't use privileged mode |
| .dockerignore exists | Excludes .env, .git, secrets |
| No ADD for remote URLs | COPY preferred over ADD |

## Performance

| Check | Pass Criteria |
|-------|---------------|
| Multi-stage build | Multiple FROM statements |
| Deps before source | COPY lock files before source code |
| Cache mounts used | --mount=type=cache for package managers |
| .dockerignore comprehensive | Excludes node_modules, __pycache__, .git, tests |
| Minimal base image | alpine, slim, or distroless variants |
| Package cache cleaned | apt-get clean or rm -rf /var/lib/apt/lists in same RUN |

## Production Readiness

| Check | Pass Criteria |
|-------|---------------|
| HEALTHCHECK defined | HEALTHCHECK instruction in Dockerfile |
| Exec form CMD | CMD uses JSON array, not shell form |
| PID 1 handling | App is PID 1 or uses tini/dumb-init |
| Restart policy | restart: unless-stopped in compose |
| Resource limits | mem_limit/cpus set in compose |
| Logging to stdout | No file-based logging in CMD |

## Compose Checks

| Check | Pass Criteria |
|-------|---------------|
| Named networks | Custom network, not default bridge |
| Health conditions | depends_on uses condition: service_healthy |
| Named volumes | No anonymous volumes |
| No hardcoded secrets | Environment uses variable references or env_file |
| Service ordering | depends_on with health checks |

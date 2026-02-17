---
name: generating-chart
description: Generate or customize a Helm chart for Kubernetes workloads. Supports batch workers (poll-then-exit), web services, and CronJobs with optional production extras (KEDA, NetworkPolicy, PDB, ServiceMonitor).
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
  - Bash(helm create *)
  - Bash(pwd)
  - Bash(basename *)
  - Bash(rm -rf *)
---

# Generate Helm Chart

Generate or customize a Helm chart for Kubernetes workloads following battle-tested patterns from production services.

## Philosophy

- **Workload-appropriate defaults** - Batch workers get exec probes and no service; web services get HTTP probes and ingress
- **Security by default** - Non-root, drop ALL capabilities, readOnlyRootFilesystem
- **Config from environment** - ConfigMap for non-sensitive, Secret (stringData) for sensitive values
- **Checksum annotations** - Auto-restart pods on config/secret changes
- **Production extras are opt-in** - KEDA, NetworkPolicy, PDB, ServiceMonitor only when requested

## Workflow

### 1. Detect Existing Chart

```text
Glob: chart/Chart.yaml, chart/values.yaml
```

- If `chart/` exists -> **customize mode** (read existing, present findings, ask what to change)
- If `chart/` doesn't exist -> **generate mode** (ask questions, run `helm create chart`, customize)

### 2. Ask Workload Type

Present via AskUserQuestion:

| Option | Description |
|--------|-------------|
| Batch worker (Recommended) | Poll-then-exit, replicaCount:0, exec probes, no service. For SQS/Kafka consumers. |
| Web service | HTTP endpoints, service, ingress, HTTP probes. For APIs and web apps. |
| CronJob | Scheduled batch, concurrencyPolicy:Forbid. For periodic tasks. |

### 3. Ask Production Extras

Present via AskUserQuestion (multiSelect: true):

| Option | Template | Description |
|--------|----------|-------------|
| KEDA ScaledObject | `scaled-object.yaml` | Queue-based autoscaling (SQS, Kafka) |
| NetworkPolicy | `network-policy.yaml` | Restrict egress to specific services |
| PodDisruptionBudget | `pdb.yaml` | Protect against voluntary disruptions |
| ServiceMonitor | `service-monitor.yaml` | Prometheus metrics scraping |
| None | -- | Core templates only |

### 4. Detect Config Patterns

Scan project files to auto-populate configmap/secrets keys:

```text
Glob: config/settings.py, config/settings.yaml, src/**/settings.py
```

For Python (Pydantic Settings):

- Extract nested model classes (AWSSettings, SQSSettings, etc.)
- Map to env vars with `__` delimiter: `AWS__AWS_REGION`, `SQS__INPUT_QUEUE`
- Separate sensitive fields (passwords, keys, tokens) -> secrets
- Non-sensitive fields -> configmap

```text
Glob: Dockerfile, pyproject.toml, package.json, go.mod
```

- Detect language for probe commands
- Detect ENTRYPOINT for exec probe command (e.g., `pgrep -f main.py`)

### 5. Load References

Read the following reference files based on selections:

| Always | `references/common-templates.md` |
|--------|----------------------------------|
| Batch worker | `references/batch-worker.md` |
| Web service | `references/web-service.md` |
| CronJob | `references/cronjob.md` |
| Any extras selected | `references/production-extras.md` |
| Generate mode | `references/helm-create-customizations.md` |

### 6. Generate Mode

#### 6a. Run `helm create chart`

```bash
helm create chart
```

#### 6b. Apply Customizations

Read `references/helm-create-customizations.md` for the removal/modification checklist.

**Batch worker customizations:**

1. Remove: `templates/service.yaml`, `templates/ingress.yaml`, `templates/hpa.yaml`, `templates/serviceaccount.yaml`, `templates/tests/`
2. Remove from values.yaml: `service`, `ingress`, `httpRoute`, `autoscaling`, `serviceAccount`, `volumes`, `volumeMounts`, `podLabels`
3. Rewrite deployment.yaml: remove ports, change probes to exec, add envFrom, add checksum annotations
4. Rename _helpers.tpl definitions from `chart` to project name
5. Add: `templates/configmap.yaml`, `templates/secrets.yaml`
6. Rewrite: `templates/NOTES.txt` for batch worker operations
7. Set values.yaml: `replicaCount: 0`, securityContext, exec livenessProbe, resources, nodeSelector, configmap, secrets

**Web service customizations:**

1. Keep: `templates/service.yaml`, optionally `templates/ingress.yaml`
2. Remove: `templates/hpa.yaml`, `templates/serviceaccount.yaml`, `templates/tests/`
3. Configure HTTP probes (`/healthz` or detected health endpoint)
4. Add: configmap.yaml, secrets.yaml, envFrom in deployment
5. Set values.yaml: `replicaCount: 1`, service config, HTTP probes

**CronJob customizations:**

1. Remove: `templates/deployment.yaml`, `templates/service.yaml`, `templates/ingress.yaml`, `templates/hpa.yaml`, `templates/serviceaccount.yaml`, `templates/tests/`
2. Create: `templates/cronjob.yaml` using container spec from reference
3. Add: configmap.yaml, secrets.yaml
4. Set values.yaml: schedule, concurrencyPolicy, history limits

#### 6c. Generate Production Extras

If any extras selected, read `references/production-extras.md` and create the corresponding template files.

### 7. Customize Mode

1. Read all files in `chart/templates/` and `chart/values.yaml`
2. Present findings:
   - What the chart has (workload type, probes, config, security)
   - What's missing from best practices
   - What's non-standard
3. Ask which customizations to apply via AskUserQuestion
4. Apply selected changes

### 8. Report

```text
Helm chart generated:

chart/
  Chart.yaml              - {name} v{version}
  values.yaml             - {workload_type} pattern
  templates/
    _helpers.tpl           - Standard helpers
    {workload_template}    - {description}
    configmap.yaml         - {n} config keys
    secrets.yaml           - stringData pattern
    NOTES.txt              - Operational notes
    {extras...}            - {descriptions}

Configuration:
  Workload: {type}
  Replicas: {count}
  Probes: {probe_type}
  Security: {security_summary}

Next steps:
  helm lint ./chart
  helm template {name} ./chart
  helm template {name} ./chart --set image.tag=test-123

To generate Makefile.deploy with build/push/deploy targets:
  /makesmith:deploy
```

### 9. Hand Off to makesmith

After chart generation, ask via AskUserQuestion:

| Option | Description |
|--------|-------------|
| Run /makesmith:deploy now | Generate Makefile.deploy with Helm deployment targets for this chart |
| Skip | I'll set up deployment separately |

If the user chooses to run it, invoke the `makesmith:generating-deploy` skill. Do NOT duplicate Makefile.deploy generation logic in helmcraft — that is makesmith's responsibility.

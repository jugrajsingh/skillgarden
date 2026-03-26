# Helm Create Customizations

What to remove and modify from `helm create chart` defaults for each workload type.

## Files to Remove

| File | Batch Worker | Web Service | CronJob | Reason |
|------|:---:|:---:|:---:|--------|
| `templates/service.yaml` | Remove | Keep | Remove | No HTTP endpoints for batch/cron |
| `templates/ingress.yaml` | Remove | Keep | Remove | No external traffic routing |
| `templates/hpa.yaml` | Remove | Remove | Remove | Use KEDA or manual scaling |
| `templates/serviceaccount.yaml` | Remove | Remove | Remove | Default service account sufficient |
| `templates/tests/` | Remove | Remove | Remove | Helm test pods not applicable |

## Files to Add

| File | All Types | Description |
|------|:---------:|-------------|
| `templates/configmap.yaml` | Add | Non-sensitive env vars from values.configmap |
| `templates/secrets.yaml` | Add | Sensitive env vars using stringData pattern |

CronJob only:

| File | Description |
|------|-------------|
| `templates/cronjob.yaml` | Replace deployment.yaml with CronJob spec |

## values.yaml Sections to Remove

| Section | Batch Worker | Web Service | CronJob | Reason |
|---------|:---:|:---:|:---:|--------|
| `serviceAccount` | Remove | Remove | Remove | Using default |
| `service` | Remove | Keep | Remove | No HTTP endpoints |
| `ingress` | Remove | Keep | Remove | No external access |
| `httpRoute` | Remove | Remove | Remove | Gateway API not needed |
| `autoscaling` | Remove | Remove | Remove | Use KEDA instead |
| `volumes` | Remove | Remove | Remove | Stateless |
| `volumeMounts` | Remove | Remove | Remove | Stateless |
| `podLabels` | Remove | Remove | Remove | Labels via _helpers.tpl |

## values.yaml Sections to Modify

| Section | Change | Reason |
|---------|--------|--------|
| `replicaCount` | Batch: `0`, Web: `1`, CronJob: remove | Batch workers are externally scaled |
| `image.repository` | Set to actual registry/image | Replace default nginx |
| `imagePullSecrets` | Set to registry secret | Authentication for private registries |
| `securityContext` | Add runAsNonRoot, drop ALL | Security hardening |
| `livenessProbe` | Batch: exec, Web: HTTP, CronJob: remove | Match workload type |
| `readinessProbe` | Batch: remove, Web: HTTP, CronJob: remove | Batch workers don't serve traffic |
| `resources` | Set actual limits | Prevent OOM/resource exhaustion |
| `nodeSelector` | Set to target nodes | Production node targeting |

## values.yaml Sections to Add

| Section | Description |
|---------|-------------|
| `configmap` | Key-value pairs for ConfigMap |
| `secrets` | Empty `{}` with commented expected keys |

## deployment.yaml Changes

| Change | Batch Worker | Web Service | Reason |
|--------|:---:|:---:|--------|
| Remove autoscaling conditional | Yes | Yes | No HPA |
| Remove serviceAccountName | Yes | Yes | Default SA |
| Remove ports section | Yes | No | No HTTP server |
| Change probes to exec | Yes | No | No HTTP endpoints |
| Remove probes entirely | No | No | CronJob only |
| Add checksum annotations | Yes | Yes | Auto-restart on config change |
| Add envFrom (configmap + secrets) | Yes | Yes | Inject all config as env vars |
| Remove volumeMounts | Yes | Yes | Stateless |
| Remove volumes | Yes | Yes | Stateless |
| Remove podLabels with block | Yes | Yes | Use selectorLabels only |

## _helpers.tpl Changes

| Change | Description |
|--------|-------------|
| Rename all `chart.*` to `{name}.*` | Match chart name |
| Remove `serviceAccountName` helper | Not used |

## NOTES.txt Changes

| Change | Description |
|--------|-------------|
| Remove HTTP URL instructions | Not applicable for batch/cron |
| Add kubectl log/status commands | Operational monitoring |
| Add scale/upgrade/delete commands | Common operations |
| Show key config values | Quick reference |

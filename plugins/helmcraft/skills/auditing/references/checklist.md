# Helm Chart Audit Checklist

## Security

| Check | Pass Criteria | Severity |
|-------|---------------|----------|
| Non-root user | `securityContext.runAsNonRoot: true` and `runAsUser` set | FAIL |
| Capabilities dropped | `securityContext.capabilities.drop: [ALL]` | FAIL |
| No secrets in values.yaml | `secrets: {}` (empty) with expected keys as comments only | FAIL |
| readOnlyRootFilesystem | `securityContext.readOnlyRootFilesystem: true` where possible | WARN |
| imagePullPolicy | `IfNotPresent` (not `Always` in prod values) | WARN |
| No privilege escalation | `securityContext.allowPrivilegeEscalation: false` | FAIL |

## Best Practices

| Check | Pass Criteria | Severity |
|-------|---------------|----------|
| Checksum annotations | `checksum/config` and `checksum/secrets` in pod annotations | WARN |
| Resource limits defined | `resources.limits` and `resources.requests` not empty `{}` | WARN |
| Labels via _helpers.tpl | Labels use `include "{name}.labels"`, not hardcoded | WARN |
| Image tag not hardcoded | Uses `{{ .Values.image.tag \| default .Chart.AppVersion }}` | WARN |
| stringData for secrets | `stringData:` preferred over `data:` + `b64enc` | WARN |
| Conditional configmap | `{{- if .Values.configmap }}` guard present | WARN |
| Conditional secrets | `{{- if .Values.secrets }}` guard present | WARN |
| Chart.yaml apiVersion | `apiVersion: v2` | WARN |

## Production Readiness

| Check | Pass Criteria | Severity |
|-------|---------------|----------|
| Probes configured | Liveness probe present (type appropriate for workload) | FAIL |
| NodeSelector defined | `nodeSelector` not empty `{}` | WARN |
| NOTES.txt customized | Not default `helm create` HTTP instructions | WARN |
| imagePullSecrets | Configured for private registry authentication | WARN |
| Name overrides | `nameOverride` and `fullnameOverride` set | WARN |

## Workload-Specific

### Batch Worker

| Check | Pass Criteria | Severity |
|-------|---------------|----------|
| No service template | `templates/service.yaml` should not exist | WARN |
| No ingress template | `templates/ingress.yaml` should not exist | WARN |
| Exec probes | Probes use `exec`, not `httpGet` | WARN |
| replicaCount zero | Default `replicaCount: 0` (externally scaled) | WARN |

### Web Service

| Check | Pass Criteria | Severity |
|-------|---------------|----------|
| Service defined | `templates/service.yaml` exists | FAIL |
| HTTP probes | Probes use `httpGet` with health endpoint | WARN |
| Container port | Deployment spec includes `ports` section | FAIL |

### CronJob

| Check | Pass Criteria | Severity |
|-------|---------------|----------|
| CronJob template | `templates/cronjob.yaml` exists | FAIL |
| No deployment | `templates/deployment.yaml` should not exist | WARN |
| concurrencyPolicy | Set to `Forbid` or `Replace` | WARN |
| History limits | `successfulJobsHistoryLimit` and `failedJobsHistoryLimit` set | WARN |

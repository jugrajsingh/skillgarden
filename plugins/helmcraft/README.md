# helmcraft

Helm chart generation for Kubernetes workloads. Encodes battle-tested patterns for batch workers, web services, and CronJobs with optional production extras.

## Skills

| Skill | Command | Description |
|-------|---------|-------------|
| `generating-chart` | `/helmcraft:chart` | Generate or customize a Helm chart |
| `auditing` | `/helmcraft:audit` | Audit chart against best practices checklist |

## Workload Types

| Type | Pattern | Key Features |
|------|---------|--------------|
| **Batch worker** | Poll-then-exit | replicaCount:0, exec probes, no service, externally scaled |
| **Web service** | HTTP server | Service + Ingress, HTTP probes, replicaCount:1 |
| **CronJob** | Scheduled batch | CronJob spec, concurrencyPolicy, history limits |

## Production Extras

Optional templates gated by `.Values.{feature}.enabled`:

- **KEDA ScaledObject** - Queue-based autoscaling (SQS, Kafka)
- **NetworkPolicy** - Restrict egress to specific services
- **PodDisruptionBudget** - Protect against voluntary disruptions
- **ServiceMonitor** - Prometheus metrics scraping

## Modes

- **Generate mode** - Runs `helm create chart`, then customizes for the selected workload type
- **Customize mode** - Reads existing `chart/`, identifies gaps, applies selected improvements

## Patterns

- **stringData for secrets** - No manual base64 encoding, Kubernetes handles it
- **Checksum annotations** - Auto-restart pods on configmap/secret changes
- **Config detection** - Scans `config/settings.py` to suggest configmap keys
- **Security by default** - Non-root, drop ALL, readOnlyRootFilesystem

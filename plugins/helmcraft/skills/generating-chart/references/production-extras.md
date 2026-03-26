# Production Extras

Optional templates for production-grade deployments. Each is gated by a `.Values.{feature}.enabled` flag.

## KEDA ScaledObject

Auto-scale based on external metrics (SQS queue depth, Kafka lag, etc.).

### values.yaml Section

```yaml
keda:
  enabled: false
  minReplicaCount: 0
  maxReplicaCount: 5
  cooldownPeriod: 300
  pollingInterval: 30
  trigger:
    type: aws-sqs-queue  # or kafka, prometheus, etc.
    metadata: {}
    # SQS example:
    #   queueURL: https://sqs.us-east-2.amazonaws.com/123456789/my-queue
    #   queueLength: "5"
    #   awsRegion: us-east-2
    # Kafka example:
    #   bootstrapServers: kafka:9092
    #   consumerGroup: my-group
    #   topic: my-topic
    #   lagThreshold: "10"
  authRef:
    name: ""  # TriggerAuthentication name if needed
```

### scaled-object.yaml

```yaml
{{- if .Values.keda.enabled }}
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: {{ include "{name}.fullname" . }}
  labels:
    {{- include "{name}.labels" . | nindent 4 }}
spec:
  scaleTargetRef:
    name: {{ include "{name}.fullname" . }}
  minReplicaCount: {{ .Values.keda.minReplicaCount }}
  maxReplicaCount: {{ .Values.keda.maxReplicaCount }}
  cooldownPeriod: {{ .Values.keda.cooldownPeriod }}
  pollingInterval: {{ .Values.keda.pollingInterval }}
  triggers:
    - type: {{ .Values.keda.trigger.type }}
      metadata:
        {{- toYaml .Values.keda.trigger.metadata | nindent 8 }}
      {{- if .Values.keda.authRef.name }}
      authenticationRef:
        name: {{ .Values.keda.authRef.name }}
      {{- end }}
{{- end }}
```

## NetworkPolicy

Restrict pod egress to only required services.

### values.yaml Section

```yaml
networkPolicy:
  enabled: false
  egress:
    # Elasticsearch
    - to:
        - namespaceSelector:
            matchLabels:
              name: elastic-system
      ports:
        - port: 9200
          protocol: TCP
    # SQS (AWS API)
    - to:
        - ipBlock:
            cidr: 0.0.0.0/0
      ports:
        - port: 443
          protocol: TCP
    # DNS
    - to: []
      ports:
        - port: 53
          protocol: UDP
        - port: 53
          protocol: TCP
```

### network-policy.yaml

```yaml
{{- if .Values.networkPolicy.enabled }}
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: {{ include "{name}.fullname" . }}
  labels:
    {{- include "{name}.labels" . | nindent 4 }}
spec:
  podSelector:
    matchLabels:
      {{- include "{name}.selectorLabels" . | nindent 6 }}
  policyTypes:
    - Egress
  egress:
    {{- toYaml .Values.networkPolicy.egress | nindent 4 }}
{{- end }}
```

## PodDisruptionBudget

Protect against voluntary disruptions (node drains, cluster upgrades).

### values.yaml Section

```yaml
pdb:
  enabled: false
  minAvailable: 1
  # maxUnavailable: 1  # Alternative to minAvailable
```

### pdb.yaml

```yaml
{{- if .Values.pdb.enabled }}
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: {{ include "{name}.fullname" . }}
  labels:
    {{- include "{name}.labels" . | nindent 4 }}
spec:
  {{- if .Values.pdb.minAvailable }}
  minAvailable: {{ .Values.pdb.minAvailable }}
  {{- end }}
  {{- if .Values.pdb.maxUnavailable }}
  maxUnavailable: {{ .Values.pdb.maxUnavailable }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "{name}.selectorLabels" . | nindent 6 }}
{{- end }}
```

## ServiceMonitor

Prometheus metrics scraping via the Prometheus Operator.

### values.yaml Section

```yaml
serviceMonitor:
  enabled: false
  interval: 30s
  path: /metrics
  port: metrics
  labels: {}
```

### service-monitor.yaml

```yaml
{{- if .Values.serviceMonitor.enabled }}
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: {{ include "{name}.fullname" . }}
  labels:
    {{- include "{name}.labels" . | nindent 4 }}
    {{- with .Values.serviceMonitor.labels }}
    {{- toYaml . | nindent 4 }}
    {{- end }}
spec:
  selector:
    matchLabels:
      {{- include "{name}.selectorLabels" . | nindent 6 }}
  endpoints:
    - port: {{ .Values.serviceMonitor.port }}
      path: {{ .Values.serviceMonitor.path }}
      interval: {{ .Values.serviceMonitor.interval }}
{{- end }}
```

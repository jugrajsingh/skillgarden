# Batch Worker Pattern

Poll-then-exit workload: reads from a queue (SQS, Kafka), processes messages, exits after consecutive blank polls. No HTTP endpoints.

## values.yaml Template

```yaml
replicaCount: 0

image:
  repository: gcr.io/{gcp_project}/{name}
  pullPolicy: IfNotPresent
  tag: ""

imagePullSecrets:
  - name: gcr-secret

nameOverride: "{name}"
fullnameOverride: "{name}"

podAnnotations: {}

podSecurityContext: {}

securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
  capabilities:
    drop:
      - ALL

# Exec probe: detect zombie/hung processes (no HTTP server)
livenessProbe:
  exec:
    command: ["pgrep", "-f", "{entrypoint}"]
  initialDelaySeconds: 10
  periodSeconds: 30
  failureThreshold: 3

resources:
  limits:
    cpu: 1
    memory: 1Gi
  requests:
    cpu: 500m
    memory: 512Mi

nodeSelector:
  collection: general

tolerations: []

affinity: {}

configmap:
  ENVIRONMENT: 'production'
  # Populate from config/settings.py sections

secrets: {}
  # Sensitive keys as comments:
  # AWS__AWS_ACCESS_KEY_ID: ""
  # AWS__AWS_SECRET_ACCESS_KEY: ""
```

## deployment.yaml Template

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "{name}.fullname" . }}
  labels:
    {{- include "{name}.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "{name}.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      annotations:
        {{- if .Values.configmap }}
        checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}
        {{- end }}
        {{- if .Values.secrets }}
        checksum/secrets: {{ include (print $.Template.BasePath "/secrets.yaml") . | sha256sum }}
        {{- end }}
        {{- with .Values.podAnnotations }}
        {{- toYaml . | nindent 8 }}
        {{- end }}
      labels:
        {{- include "{name}.selectorLabels" . | nindent 8 }}
    spec:
      {{- with .Values.imagePullSecrets }}
      imagePullSecrets:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      securityContext:
        {{- toYaml .Values.podSecurityContext | nindent 8 }}
      containers:
        - name: {{ .Chart.Name }}
          securityContext:
            {{- toYaml .Values.securityContext | nindent 12 }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          {{- with .Values.livenessProbe }}
          livenessProbe:
            {{- toYaml . | nindent 12 }}
          {{- end }}
          {{- if or .Values.configmap .Values.secrets }}
          envFrom:
            {{- if .Values.configmap }}
            - configMapRef:
                name: '{{ include "{name}.fullname" . }}-configmap'
            {{- end }}
            {{- if .Values.secrets }}
            - secretRef:
                name: '{{ include "{name}.fullname" . }}-secrets'
            {{- end }}
          {{- end }}
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
      {{- with .Values.nodeSelector }}
      nodeSelector:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.affinity }}
      affinity:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.tolerations }}
      tolerations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
```

## Key Characteristics

- **No ports** - Container doesn't listen on any port
- **No service/ingress** - Purely outbound connections (queue, database, ES)
- **Exec probes** - `pgrep -f main.py` or similar process check
- **replicaCount: 0** - Externally scaled (KEDA, manual, CI/CD)
- **Checksum annotations** - Auto-restart on configmap/secret changes
- **envFrom** - All config injected as environment variables

## NOTES.txt Template

```text
{name} has been deployed.

Release: {{ .Release.Name }}
Namespace: {{ .Release.Namespace }}
Image: {{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}
Replicas: {{ .Values.replicaCount }}

To view logs:
  kubectl logs -f -l app.kubernetes.io/name={{ include "{name}.name" . }} -n {{ .Release.Namespace }}

To check pod status:
  kubectl get pods -l app.kubernetes.io/name={{ include "{name}.name" . }} -n {{ .Release.Namespace }}

To scale up:
  kubectl scale deployment {{ include "{name}.fullname" . }} --replicas=1 -n {{ .Release.Namespace }}

To update:
  helm upgrade {{ .Release.Name }} ./chart --set image.tag=<new-tag>

To delete:
  helm delete {{ .Release.Name }} -n {{ .Release.Namespace }}
```

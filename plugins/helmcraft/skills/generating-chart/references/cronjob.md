# CronJob Pattern

Scheduled batch workload: runs on a cron schedule, processes a task, exits. No long-running pods.

## values.yaml Template

```yaml
image:
  repository: gcr.io/{gcp_project}/{name}
  pullPolicy: IfNotPresent
  tag: ""

imagePullSecrets:
  - name: {secret-name}

nameOverride: "{name}"
fullnameOverride: "{name}"

cronjob:
  schedule: "0 2 * * 1"  # Weekly Monday 2am UTC
  concurrencyPolicy: Forbid
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
  backoffLimit: 2
  activeDeadlineSeconds: 3600  # 1 hour max
  restartPolicy: Never

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

secrets: {}
```

## cronjob.yaml Template

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: {{ include "{name}.fullname" . }}
  labels:
    {{- include "{name}.labels" . | nindent 4 }}
spec:
  schedule: {{ .Values.cronjob.schedule | quote }}
  concurrencyPolicy: {{ .Values.cronjob.concurrencyPolicy }}
  successfulJobsHistoryLimit: {{ .Values.cronjob.successfulJobsHistoryLimit }}
  failedJobsHistoryLimit: {{ .Values.cronjob.failedJobsHistoryLimit }}
  jobTemplate:
    spec:
      {{- if .Values.cronjob.activeDeadlineSeconds }}
      activeDeadlineSeconds: {{ .Values.cronjob.activeDeadlineSeconds }}
      {{- end }}
      backoffLimit: {{ .Values.cronjob.backoffLimit }}
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
            {{- toYaml . | nindent 12 }}
            {{- end }}
          labels:
            {{- include "{name}.selectorLabels" . | nindent 12 }}
        spec:
          {{- with .Values.imagePullSecrets }}
          imagePullSecrets:
            {{- toYaml . | nindent 12 }}
          {{- end }}
          securityContext:
            {{- toYaml .Values.podSecurityContext | nindent 12 }}
          restartPolicy: {{ .Values.cronjob.restartPolicy }}
          containers:
            - name: {{ .Chart.Name }}
              securityContext:
                {{- toYaml .Values.securityContext | nindent 16 }}
              image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
              imagePullPolicy: {{ .Values.image.pullPolicy }}
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
                {{- toYaml .Values.resources | nindent 16 }}
          {{- with .Values.nodeSelector }}
          nodeSelector:
            {{- toYaml . | nindent 12 }}
          {{- end }}
          {{- with .Values.affinity }}
          affinity:
            {{- toYaml . | nindent 12 }}
          {{- end }}
          {{- with .Values.tolerations }}
          tolerations:
            {{- toYaml . | nindent 12 }}
          {{- end }}
```

## Key Characteristics

- **No Deployment** - Uses CronJob instead
- **No Service/Ingress** - No HTTP endpoints
- **No probes** - Short-lived pods, not needed
- **concurrencyPolicy: Forbid** - Prevents overlapping runs
- **restartPolicy: Never** - Failed jobs create new pods via backoffLimit
- **activeDeadlineSeconds** - Hard timeout to prevent runaway jobs
- **History limits** - Keep recent job history for debugging

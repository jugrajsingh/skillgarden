# Web Service Pattern

HTTP-serving workload: exposes endpoints via Service and optional Ingress. Uses HTTP probes for health checking.

## values.yaml Template

```yaml
replicaCount: 1

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
  capabilities:
    drop:
      - ALL

service:
  type: ClusterIP
  port: 80
  targetPort: 8000

ingress:
  enabled: false
  className: ""
  annotations: {}
  hosts:
    - host: {name}.example.com
      paths:
        - path: /
          pathType: ImplementationSpecific
  tls: []

livenessProbe:
  httpGet:
    path: /healthz
    port: http
  initialDelaySeconds: 10
  periodSeconds: 15
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /healthz
    port: http
  initialDelaySeconds: 5
  periodSeconds: 10
  failureThreshold: 3

resources:
  limits:
    cpu: 1
    memory: 1Gi
  requests:
    cpu: 250m
    memory: 256Mi

nodeSelector:
  collection: general

tolerations: []

affinity: {}

configmap:
  ENVIRONMENT: 'production'

secrets: {}
```

## deployment.yaml Differences from Batch Worker

```yaml
# Adds container port
ports:
  - name: http
    containerPort: {{ .Values.service.targetPort }}
    protocol: TCP

# HTTP probes instead of exec
livenessProbe:
  {{- toYaml .Values.livenessProbe | nindent 12 }}
readinessProbe:
  {{- toYaml .Values.readinessProbe | nindent 12 }}
```

## service.yaml Template

```yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ include "{name}.fullname" . }}
  labels:
    {{- include "{name}.labels" . | nindent 4 }}
spec:
  type: {{ .Values.service.type }}
  ports:
    - port: {{ .Values.service.port }}
      targetPort: {{ .Values.service.targetPort }}
      protocol: TCP
      name: http
  selector:
    {{- include "{name}.selectorLabels" . | nindent 4 }}
```

## ingress.yaml Template

```yaml
{{- if .Values.ingress.enabled -}}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ include "{name}.fullname" . }}
  labels:
    {{- include "{name}.labels" . | nindent 4 }}
  {{- with .Values.ingress.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
spec:
  {{- if .Values.ingress.className }}
  ingressClassName: {{ .Values.ingress.className }}
  {{- end }}
  {{- if .Values.ingress.tls }}
  tls:
    {{- range .Values.ingress.tls }}
    - hosts:
        {{- range .hosts }}
        - {{ . | quote }}
        {{- end }}
      secretName: {{ .secretName }}
    {{- end }}
  {{- end }}
  rules:
    {{- range .Values.ingress.hosts }}
    - host: {{ .host | quote }}
      http:
        paths:
          {{- range .paths }}
          - path: {{ .path }}
            pathType: {{ .pathType }}
            backend:
              service:
                name: {{ include "{name}.fullname" $ }}
                port:
                  number: {{ $.Values.service.port }}
          {{- end }}
    {{- end }}
{{- end }}
```

## Key Characteristics

- **Service exposed** - ClusterIP by default, configurable
- **HTTP probes** - `/healthz` endpoint for liveness and readiness
- **Container port** - Declared in deployment spec
- **Ingress optional** - Disabled by default, enable with `ingress.enabled: true`
- **replicaCount: 1** - Always-on by default

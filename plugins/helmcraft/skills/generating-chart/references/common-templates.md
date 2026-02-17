# Common Templates

Shared templates used by all workload types.

## _helpers.tpl

Replace `{name}` with the chart name throughout.

```yaml
{{/*
Expand the name of the chart.
*/}}
{{- define "{name}.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "{name}.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "{name}.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "{name}.labels" -}}
helm.sh/chart: {{ include "{name}.chart" . }}
{{ include "{name}.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "{name}.selectorLabels" -}}
app.kubernetes.io/name: {{ include "{name}.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
```

## configmap.yaml

```yaml
{{- if .Values.configmap }}
apiVersion: v1
kind: ConfigMap
metadata:
  name: '{{ include "{name}.fullname" . }}-configmap'
  labels:
    {{- include "{name}.labels" . | nindent 4 }}
data:
  {{- toYaml .Values.configmap | nindent 2 }}
{{- end }}
```

## secrets.yaml (stringData Pattern)

Uses `stringData` instead of `data` + `b64enc`. Kubernetes handles base64 encoding automatically. Includes `{{- if $value }}` guard to skip empty values.

```yaml
{{- if .Values.secrets }}
apiVersion: v1
kind: Secret
metadata:
  name: '{{ include "{name}.fullname" . }}-secrets'
  labels:
    {{- include "{name}.labels" . | nindent 4 }}
type: Opaque
stringData:
  {{- range $key, $value := .Values.secrets }}
  {{- if $value }}
  {{ $key }}: {{ $value | quote }}
  {{- end }}
  {{- end }}
{{- end }}
```

### Why stringData Over data + b64enc

| Aspect | `data` + `b64enc` | `stringData` |
|--------|--------------------|--------------|
| Values file | Plain text | Plain text |
| Template | `{{ $value \| b64enc \| quote }}` | `{{ $value \| quote }}` |
| Empty handling | Encodes empty string | Skip with `{{- if $value }}` |
| Kubernetes | Stored as base64 | Auto-encoded to base64 |
| Debugging | Must decode to read | Plain in template output |

## Chart.yaml

```yaml
apiVersion: v2
name: {name}
description: {description}
type: application
version: 0.1.0
appVersion: "0.1.0"
```

## NOTES.txt

Customize per workload type. See workload-specific reference files for templates.

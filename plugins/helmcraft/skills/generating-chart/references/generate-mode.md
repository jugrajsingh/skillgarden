# Generate Mode Customizations

## 6a. Run `helm create chart`

```bash
helm create chart
```

## 6b. Apply Customizations

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

## 6c. Generate Production Extras

If any extras selected, read `references/production-extras.md` and create the corresponding template files.

# kubectl Deployment Targets

Targets for deploying to Kubernetes via raw manifests (no Helm).

## Targets

```makefile
# =============================================================================
# Kubernetes Deployment (kubectl)
# =============================================================================

MANIFESTS_DIR := k8s
NAMESPACE ?= default
KUBE_CONTEXT ?= {kube_context}

deploy:  ## Apply Kubernetes manifests
 kubectl apply -f $(MANIFESTS_DIR)/ --namespace $(NAMESPACE) --context $(KUBE_CONTEXT)

deploy-dry-run:  ## Dry run deployment
 kubectl apply -f $(MANIFESTS_DIR)/ --namespace $(NAMESPACE) --context $(KUBE_CONTEXT) --dry-run=client

undeploy:  ## Delete Kubernetes resources
 kubectl delete -f $(MANIFESTS_DIR)/ --namespace $(NAMESPACE) --context $(KUBE_CONTEXT) || true

redeploy: undeploy  ## Delete and reapply
 @sleep 5
 $(MAKE) -f Makefile.deploy deploy

build-push-deploy: build-and-push deploy  ## Full CI/CD: build, push, deploy

# =============================================================================
# Image Update (without full redeploy)
# =============================================================================

rolling-update:  ## Update deployment image tag
 kubectl set image deployment/$(IMAGE_NAME) \
  $(IMAGE_NAME)=$(REGISTRY)/$(IMAGE_NAME):$(VERSION) \
  --namespace $(NAMESPACE) --context $(KUBE_CONTEXT)

# =============================================================================
# Status & Operations
# =============================================================================

status:  ## Show pod status
 kubectl get pods -n $(NAMESPACE) -l app=$(IMAGE_NAME) --context $(KUBE_CONTEXT)

logs:  ## Tail pod logs
 kubectl logs -f -n $(NAMESPACE) -l app=$(IMAGE_NAME) --context $(KUBE_CONTEXT) --tail=100

rollback:  ## Rollback deployment
 kubectl rollout undo deployment/$(IMAGE_NAME) --namespace $(NAMESPACE) --context $(KUBE_CONTEXT)

history:  ## Show rollout history
 kubectl rollout history deployment/$(IMAGE_NAME) --namespace $(NAMESPACE) --context $(KUBE_CONTEXT)
```

## Manifest Template

Generate a basic deployment manifest at `k8s/deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {project_name}
  labels:
    app: {project_name}
spec:
  replicas: 1
  selector:
    matchLabels:
      app: {project_name}
  template:
    metadata:
      labels:
        app: {project_name}
    spec:
      containers:
        - name: {project_name}
          image: {registry}/{project_name}:latest
          ports:
            - containerPort: {port}
```

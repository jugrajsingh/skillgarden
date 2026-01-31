---
name: generating-deploy
description: Generate Makefile.deploy with DevOps targets for building, pushing, and deploying Docker images via Helm/kubectl. Supports multi-registry tag-on-push and per-pipeline deployments.
allowed-tools:
  - Read
  - Write
  - Glob
  - AskUserQuestion
  - Bash(pwd)
  - Bash(basename *)
  - Bash(git describe *)
---

# Generate Makefile.deploy

Generate Makefile.deploy with DevOps targets for Docker and Kubernetes deployments.

## Philosophy

- **Makefile.deploy for DevOps** - Build, push, deploy commands
- **Separate from local dev** - Makefile.local for development
- **Multi-registry support** - GCR, ECR, ACR, DockerHub
- **Tag-on-push pattern** - Build tags locally, push tags for registry
- **Helm-based deployment** - Kubernetes via Helm charts
- **Version from git** - Use git describe for image tags

## Workflow

### 1. Detect Project Info

```bash
basename $(pwd)
git describe --tags --always 2>/dev/null || echo "latest"
```

### 2. Ask About Container Registry

Present via AskUserQuestion:

```text
Which container registry will you use?

○ GCR (Google Container Registry)
○ ECR (AWS Elastic Container Registry)
○ ACR (Azure Container Registry)
○ DockerHub
○ Custom registry
```

### 3. Ask About Deployment Target

Present via AskUserQuestion:

```text
How will you deploy?

○ Helm (Kubernetes via Helm charts)
○ kubectl (direct Kubernetes manifests)
○ Docker Compose (remote server)
○ None (just build and push)
```

### 4. Ask About Multi-Pipeline Support

Present via AskUserQuestion:

```text
Does this project have multiple deployment pipelines?

○ Single pipeline (one deploy target)
○ Multiple pipelines (e.g., crawl, process, export)
```

If multiple, ask for pipeline names.

### 5. Generate Makefile.deploy

```makefile
# =============================================================================
# Makefile.deploy - DevOps Commands
# =============================================================================
# Usage: make -f Makefile.deploy <target>
# Help:  make -f Makefile.deploy help
# =============================================================================

# Project configuration
IMAGE_NAME := {project_name}
VERSION := $(shell git describe --tags --always 2>/dev/null || echo "latest")
RELEASE_NAME := {project_name}

# Kubernetes configuration
NAMESPACE := default
KUBE_CONTEXT := {kube_context}

# Container Registries
GCR_REGISTRY := gcr.io/{gcp_project}
ECR_REGISTRY := {aws_account_id}.dkr.ecr.{region}.amazonaws.com
ACR_REGISTRY := {acr_name}.azurecr.io

.DEFAULT_GOAL := help

.PHONY: help version build-image push-image-gcr push-image-ecr push-image-acr \
        push-image build-and-push gcr-login ecr-login acr-login \
        deploy redeploy helm-lint helm-template helm-dry-run \
        leaks query-image-size

# =============================================================================
# Info
# =============================================================================

help:  ## Show available targets
 @grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'

version:  ## Show current version
 @echo "Image: $(IMAGE_NAME):$(VERSION)"

# =============================================================================
# Docker Build (local tag only)
# =============================================================================

build-image:  ## Build Docker image (local tag only)
 @echo "Building $(IMAGE_NAME):$(VERSION)..."
 docker build -t $(IMAGE_NAME):$(VERSION) .

query-image-size:  ## Show Docker image size
 @docker images $(IMAGE_NAME):$(VERSION) --format "Size: {{.Size}}"

# =============================================================================
# Push (tag-on-push pattern: tag for registry + push)
# =============================================================================

push-image-gcr:  ## Tag and push to GCR
 docker tag $(IMAGE_NAME):$(VERSION) $(GCR_REGISTRY)/$(IMAGE_NAME):$(VERSION)
 docker push $(GCR_REGISTRY)/$(IMAGE_NAME):$(VERSION)

push-image-ecr:  ## Tag and push to ECR
 docker tag $(IMAGE_NAME):$(VERSION) $(ECR_REGISTRY)/$(IMAGE_NAME):$(VERSION)
 docker push $(ECR_REGISTRY)/$(IMAGE_NAME):$(VERSION)

push-image-acr:  ## Tag and push to ACR
 docker tag $(IMAGE_NAME):$(VERSION) $(ACR_REGISTRY)/$(IMAGE_NAME):$(VERSION)
 docker push $(ACR_REGISTRY)/$(IMAGE_NAME):$(VERSION)

push-image: push-image-{default_registry}  ## Push to default registry

build-and-push: build-image push-image  ## Build and push to default registry

# =============================================================================
# Registry Login
# =============================================================================

gcr-login:  ## Login to GCR
 gcloud auth configure-docker gcr.io --quiet

ecr-login:  ## Login to ECR
 aws ecr get-login-password --region {region} | docker login --username AWS --password-stdin $(ECR_REGISTRY)

acr-login:  ## Login to ACR
 az acr login --name {acr_name}

# =============================================================================
# Helm Deployment (private targets for reuse)
# =============================================================================

_deploy-release:  ## (private) Deploy a Helm release
 helm upgrade --install $(RELEASE_NAME) ./chart \
  --namespace $(NAMESPACE) \
  --kube-context $(KUBE_CONTEXT) \
  --set image.repository=$(REGISTRY)/$(IMAGE_NAME) \
  --set image.tag=$(VERSION) \
  $(HELM_EXTRA_ARGS)

_purge-release:  ## (private) Uninstall a Helm release
 helm uninstall $(RELEASE_NAME) --namespace $(NAMESPACE) --kube-context $(KUBE_CONTEXT) || true

deploy: _deploy-release  ## Deploy with Helm

redeploy: _purge-release  ## Uninstall and redeploy
 @sleep 5
 $(MAKE) -f Makefile.deploy _deploy-release

build-push-deploy: build-and-push deploy  ## Full CI/CD: build, push, deploy

# =============================================================================
# Helm Utilities
# =============================================================================

helm-lint:  ## Lint Helm chart
 helm lint ./chart

helm-template:  ## Render Helm templates locally
 helm template $(RELEASE_NAME) ./chart \
  --set image.repository=$(REGISTRY)/$(IMAGE_NAME) \
  --set image.tag=$(VERSION)

helm-dry-run:  ## Dry run Helm deployment
 helm upgrade --install $(RELEASE_NAME) ./chart \
  --namespace $(NAMESPACE) \
  --kube-context $(KUBE_CONTEXT) \
  --set image.repository=$(REGISTRY)/$(IMAGE_NAME) \
  --set image.tag=$(VERSION) \
  --dry-run

# =============================================================================
# Status
# =============================================================================

status:  ## Show deployment status
 kubectl get pods -n $(NAMESPACE) -l app=$(RELEASE_NAME) --context $(KUBE_CONTEXT)

logs:  ## Tail pod logs
 kubectl logs -f -n $(NAMESPACE) -l app=$(RELEASE_NAME) --context $(KUBE_CONTEXT) --tail=100

rollback:  ## Rollback to previous release
 helm rollback $(RELEASE_NAME) --namespace $(NAMESPACE) --kube-context $(KUBE_CONTEXT)

history:  ## Show deployment history
 helm history $(RELEASE_NAME) --namespace $(NAMESPACE) --kube-context $(KUBE_CONTEXT)

# =============================================================================
# Utilities
# =============================================================================

leaks:  ## Scan for secrets with gitleaks
 @echo "Scanning for secrets..."
 gitleaks detect --source . --verbose

git-flow-release-finish:  ## Finish current git-flow release
 git flow finish --tag
```

### Per-Pipeline Targets (Multi-Pipeline)

When user selects multiple pipelines, generate additional targets per pipeline:

```makefile
# =============================================================================
# Per-Pipeline Deployment
# =============================================================================

deploy-{pipeline}: RELEASE_NAME := {project}-{pipeline}
deploy-{pipeline}: HELM_EXTRA_ARGS := -f chart/values-{pipeline}.yaml
deploy-{pipeline}: _deploy-release  ## Deploy {pipeline} pipeline

re-deploy-{pipeline}: RELEASE_NAME := {project}-{pipeline}
re-deploy-{pipeline}: _purge-release  ## Re-deploy {pipeline} pipeline
 @sleep 5
 $(MAKE) -f Makefile.deploy deploy-{pipeline}

template-{pipeline}: RELEASE_NAME := {project}-{pipeline}
template-{pipeline}: HELM_EXTRA_ARGS := -f chart/values-{pipeline}.yaml
template-{pipeline}:  ## Render templates for {pipeline}
 helm template $(RELEASE_NAME) ./chart \
  --set image.repository=$(REGISTRY)/$(IMAGE_NAME) \
  --set image.tag=$(VERSION) \
  $(HELM_EXTRA_ARGS)

build-push-deploy-{pipeline}: build-and-push deploy-{pipeline}  ## Full CI/CD for {pipeline}
```

### 6. Report

```text
Created Makefile.deploy:

Configuration:
  - Image: {project}:{version}
  - Registry: {registry_type}
  - Deployment: {deployment_type}

Targets:
  Build:
    build-image        - Build Docker image (local tag)
    push-image         - Push to default registry
    build-and-push     - Build and push

  Deploy:
    deploy             - Deploy with Helm
    redeploy           - Uninstall and redeploy
    build-push-deploy  - Full CI/CD pipeline

  Utilities:
    helm-lint          - Lint Helm chart
    helm-dry-run       - Preview deployment
    status             - Show pod status
    logs               - Tail pod logs

Usage:
  make -f Makefile.deploy build-push-deploy
```

## Registry-Specific Login Commands

**GCR (Google):**

```bash
gcloud auth configure-docker gcr.io --quiet
```

**ECR (AWS):**

```bash
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com
```

**ACR (Azure):**

```bash
az acr login --name myregistry
```

**DockerHub:**

```bash
docker login
```

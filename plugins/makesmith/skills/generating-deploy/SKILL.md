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

### 4. Ask About One-to-Many Deployments

Only if deployment target is Helm or kubectl:

```text
Does this project deploy the same image as multiple releases?

○ Single deployment (one release)
○ Multiple deployments (e.g., service-type1, service-type2, service-type3)
```

If multiple, ask for deployment names.

### 5. Load Deployment Reference

Read ONLY the reference file matching the user's deployment target choice:

| Deployment Target | Reference File |
|-------------------|----------------|
| Helm | `references/helm.md` |
| kubectl | `references/kubectl.md` |
| Docker Compose | `references/compose.md` |
| None | No reference needed |

### 6. Generate Makefile.deploy

Compose the file using the common sections below plus deployment targets from the loaded reference.

#### Common Header

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

.DEFAULT_GOAL := help
```

#### Common Targets

```makefile
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
```

Only include push targets for registries the user selected. Include registry variables for selected registries:

```makefile
# Container Registries (include only selected)
GCR_REGISTRY := gcr.io/{gcp_project}
ECR_REGISTRY := {aws_account_id}.dkr.ecr.{region}.amazonaws.com
ACR_REGISTRY := {acr_name}.azurecr.io
```

#### Deployment Targets

Insert the deployment targets from the loaded reference file. For one-to-many deployments, use the multi-deployment section from the reference.

#### Utilities

```makefile
# =============================================================================
# Utilities
# =============================================================================

leaks:  ## Scan for secrets with gitleaks
 @echo "Scanning for secrets..."
 gitleaks detect --source . --verbose

git-flow-release-finish:  ## Finish current git-flow release
 git flow finish --tag
```

### 7. Report

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
    {deployment_targets_summary}

  Utilities:
    {utility_targets_summary}

Usage:
  make -f Makefile.deploy build-push-deploy
```

## Registry Login Commands

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

## Deployment Reference Files

Each deployment method is defined in its own reference file under `references/`:

- `references/helm.md` - Helm charts with define macros and multi-pipeline support
- `references/kubectl.md` - Raw Kubernetes manifests with rolling updates
- `references/compose.md` - Docker Compose over SSH for remote servers

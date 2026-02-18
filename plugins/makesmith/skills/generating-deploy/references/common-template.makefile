# =============================================================================
# Makefile.deploy - DevOps Commands
# =============================================================================
# Usage: make -f Makefile.deploy <target>
# Help:  make -f Makefile.deploy help
# =============================================================================

# Project configuration
IMAGE_NAME := {project_name}
VERSION := $(shell git describe --tags --always 2>/dev/null || echo "latest")

# Container Registries (include only selected)
GCR_REGISTRY := gcr.io/{gcp_project}
ECR_REGISTRY := {aws_account_id}.dkr.ecr.{region}.amazonaws.com
ACR_REGISTRY := {acr_name}.azurecr.io

.DEFAULT_GOAL := help

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
# Utilities
# =============================================================================

leaks:  ## Scan for secrets with gitleaks
	@echo "Scanning for secrets..."
	gitleaks detect --source . --verbose

git-flow-release-finish:  ## Finish current git-flow release
	git flow finish --tag

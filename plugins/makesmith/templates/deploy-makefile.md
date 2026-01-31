# Makefile.deploy Reference Template

Annotated reference for DevOps Makefile with multi-registry tag-on-push pattern.

## Variables

```makefile
IMAGE_NAME := {PROJECT_NAME}
VERSION := $(shell git describe --tags --always 2>/dev/null || echo "latest")
```

## Tag-on-Push Pattern

Build creates a local-only tag. Push creates registry-prefixed tag and pushes.

```makefile
# Local build (no registry prefix)
build-image:
 docker build -t $(IMAGE_NAME):$(VERSION) .

# Push to specific registry (tag + push)
push-image-gcr:
 docker tag $(IMAGE_NAME):$(VERSION) $(GCR_REGISTRY)/$(IMAGE_NAME):$(VERSION)
 docker push $(GCR_REGISTRY)/$(IMAGE_NAME):$(VERSION)
```

## Private Helm Targets

Internal targets prefixed with underscore, reused by per-pipeline targets.

```makefile
_deploy-release:
 helm upgrade --install $(RELEASE_NAME) ./chart \
  --namespace $(NAMESPACE) \
  $(HELM_EXTRA_ARGS)

deploy-{PIPELINE}: RELEASE_NAME := {PROJECT}-{PIPELINE}
deploy-{PIPELINE}: HELM_EXTRA_ARGS := -f chart/values-{PIPELINE}.yaml
deploy-{PIPELINE}: _deploy-release
```

## Per-Pipeline Pattern

Each pipeline overrides RELEASE_NAME and HELM_EXTRA_ARGS via target-specific variables.

## Placeholders

| Placeholder | Description |
|-------------|-------------|
| {PROJECT_NAME} | Project name from basename |
| {PIPELINE} | Pipeline name (crawl, process, export) |
| {GCR_REGISTRY} | gcr.io/{gcp_project} |
| {ECR_REGISTRY} | {account}.dkr.ecr.{region}.amazonaws.com |
| {ACR_REGISTRY} | {name}.azurecr.io |

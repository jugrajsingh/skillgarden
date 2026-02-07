# Helm Deployment Targets

Targets for deploying to Kubernetes via Helm charts.

## Single Deployment Targets

```makefile
# =============================================================================
# Helm Deployment
# =============================================================================

define deploy_release
 helm upgrade --install $(1) ./chart \
  --kube-context $(KUBE_CONTEXT) \
  --namespace $(NAMESPACE) \
  --values ./chart/values.yaml \
  --values ./$(2) \
  --set image.tag=$(VERSION) \
  --wait
endef

define purge_release
 helm uninstall $(1) \
  --kube-context $(KUBE_CONTEXT) \
  --namespace $(NAMESPACE) \
  || true
endef

define template_release
 helm template $(1) ./chart \
  --values ./chart/values.yaml \
  --values ./$(2) \
  --set image.tag=$(VERSION)
endef

deploy:  ## Deploy with Helm
 $(call deploy_release,$(RELEASE_NAME),{values_file})

redeploy:  ## Uninstall and redeploy
 $(call purge_release,$(RELEASE_NAME))
 $(call deploy_release,$(RELEASE_NAME),{values_file})

build-push-deploy: build-and-push deploy  ## Full CI/CD: build, push, deploy

# =============================================================================
# Helm Utilities
# =============================================================================

helm-lint:  ## Lint Helm chart
 helm lint ./chart

helm-template:  ## Render Helm templates locally
 $(call template_release,$(RELEASE_NAME),{values_file})

helm-dry-run:  ## Dry run Helm deployment
 helm upgrade --install $(RELEASE_NAME) ./chart \
  --kube-context $(KUBE_CONTEXT) \
  --namespace $(NAMESPACE) \
  --values ./chart/values.yaml \
  --values ./{values_file} \
  --set image.tag=$(VERSION) \
  --dry-run

# =============================================================================
# Status & Operations
# =============================================================================

status:  ## Show deployment status
 kubectl get pods -n $(NAMESPACE) -l app.kubernetes.io/name=$(RELEASE_NAME) --context $(KUBE_CONTEXT)

logs:  ## Tail pod logs
 kubectl logs -f -n $(NAMESPACE) -l app.kubernetes.io/name=$(RELEASE_NAME) --context $(KUBE_CONTEXT) --tail=100

rollback:  ## Rollback to previous release
 helm rollback $(RELEASE_NAME) --namespace $(NAMESPACE) --kube-context $(KUBE_CONTEXT)

history:  ## Show deployment history
 helm history $(RELEASE_NAME) --namespace $(NAMESPACE) --kube-context $(KUBE_CONTEXT)
```

## One-to-Many Deployments

When the same codebase has multiple deployments (e.g., same image deployed as service-type1, service-type2, service-type3), each deployment has its own Helm release name and values override file.

### Using private targets with target-specific variables (1-2 deployments)

For a small number of deployments, use private `_` prefixed targets with target-specific variable overrides:

```makefile
# =============================================================================
# Private Targets (reusable via target-specific variables)
# =============================================================================

_deploy-release:  ## (private) Deploy a Helm release
 helm upgrade --install $(RELEASE_NAME) ./chart \
  --namespace $(NAMESPACE) \
  --kube-context $(KUBE_CONTEXT) \
  --set image.tag=$(VERSION) \
  --wait \
  $(HELM_EXTRA_ARGS)

_purge-release:  ## (private) Uninstall a Helm release
 helm uninstall $(RELEASE_NAME) --namespace $(NAMESPACE) --kube-context $(KUBE_CONTEXT) || true

# --- {Deployment Name} ---
deploy-{deployment}: RELEASE_NAME := {project}-{deployment}
deploy-{deployment}: HELM_EXTRA_ARGS := --values ./chart/values-{deployment}.yaml
deploy-{deployment}: _deploy-release  ## Deploy {deployment}

re-deploy-{deployment}: RELEASE_NAME := {project}-{deployment}
re-deploy-{deployment}: _purge-release  ## Re-deploy {deployment}
 @sleep 5
 $(MAKE) -f Makefile.deploy deploy-{deployment}

template-{deployment}: RELEASE_NAME := {project}-{deployment}
template-{deployment}: HELM_EXTRA_ARGS := --values ./chart/values-{deployment}.yaml
template-{deployment}:  ## Render templates for {deployment}
 helm template $(RELEASE_NAME) ./chart \
  --set image.tag=$(VERSION) \
  $(HELM_EXTRA_ARGS)

ship-{deployment}: build-and-push deploy-{deployment}  ## Build, push, deploy {deployment}
```

### Using define macros (recommended for 3+ deployments)

For many deployments, define macros reduce repetition — the deploy/purge/template logic is written once and called with arguments:

```makefile
# --- {Deployment Name} ---
deploy-{deployment}:  ## Deploy {deployment}
 $(call deploy_release,$(RELEASE_NAME)-{deployment},chart/values-{deployment}.yaml)

re-deploy-{deployment}:  ## Purge and redeploy {deployment}
 $(call purge_release,$(RELEASE_NAME)-{deployment})
 $(call deploy_release,$(RELEASE_NAME)-{deployment},chart/values-{deployment}.yaml)

template-{deployment}:  ## Render Helm templates for {deployment}
 $(call template_release,$(RELEASE_NAME)-{deployment},chart/values-{deployment}.yaml)

ship-{deployment}: build-and-push deploy-{deployment}  ## Build, push, deploy {deployment}
```

### deploy-all target

```makefile
deploy-all: deploy-{deployment1} deploy-{deployment2} deploy-{deployment3}  ## Deploy all
```

## Required Variables

```makefile
RELEASE_NAME := {project_name}
NAMESPACE ?= default
KUBE_CONTEXT ?= {kube_context}
```

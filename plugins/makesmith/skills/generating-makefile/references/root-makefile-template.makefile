# =============================================================================
# Makefile - {PROJECT_NAME}
# =============================================================================

.DEFAULT_GOAL := help

.PHONY: help install test lint format clean run

# =============================================================================
# Help
# =============================================================================

help:  ## Show available targets
	@echo ""
	@echo "╔══════════════════════════════════════════════╗"
	@echo "║  {PROJECT_NAME}                              ║"
	@echo "╠══════════════════════════════════════════════╣"
	@echo "║  Development: make -f Makefile.local help    ║"
	@echo "║  Deployment:  make -f Makefile.deploy help   ║"
	@echo "╚══════════════════════════════════════════════╝"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# =============================================================================
# Development (delegates to Makefile.local)
# =============================================================================

install:  ## Install all dependencies
	$(MAKE) -f Makefile.local install-dev

test:  ## Run tests
	$(MAKE) -f Makefile.local test

lint:  ## Run linter
	$(MAKE) -f Makefile.local lint

format:  ## Format code
	$(MAKE) -f Makefile.local format

clean:  ## Remove build artifacts
	$(MAKE) -f Makefile.local clean

# =============================================================================
# Quick Run (project-specific)
# =============================================================================

run:  ## Run the application
	$(MAKE) -f Makefile.local run

# =============================================================================
# Deployment (delegates to Makefile.deploy)
# =============================================================================

build:  ## Build Docker image
	$(MAKE) -f Makefile.deploy build-image

push:  ## Push image to registry
	$(MAKE) -f Makefile.deploy push-image

deploy:  ## Deploy to Kubernetes
	$(MAKE) -f Makefile.deploy deploy

ship: build push deploy  ## Full CI/CD: build, push, deploy

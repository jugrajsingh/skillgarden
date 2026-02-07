# Docker Compose Remote Deployment Targets

Targets for deploying to a remote server via Docker Compose over SSH.

## Targets

```makefile
# =============================================================================
# Docker Compose Deployment (Remote)
# =============================================================================

REMOTE_HOST ?= {remote_host}
REMOTE_USER ?= {remote_user}
COMPOSE_FILE := docker-compose.prod.yml

deploy:  ## Deploy to remote server
 DOCKER_HOST="ssh://$(REMOTE_USER)@$(REMOTE_HOST)" docker compose -f $(COMPOSE_FILE) up -d

deploy-build:  ## Build and deploy on remote
 DOCKER_HOST="ssh://$(REMOTE_USER)@$(REMOTE_HOST)" docker compose -f $(COMPOSE_FILE) up -d --build

undeploy:  ## Stop remote deployment
 DOCKER_HOST="ssh://$(REMOTE_USER)@$(REMOTE_HOST)" docker compose -f $(COMPOSE_FILE) down

build-push-deploy: build-and-push  ## Build, push, pull and restart on remote
 ssh $(REMOTE_USER)@$(REMOTE_HOST) "cd /opt/$(IMAGE_NAME) && docker compose -f $(COMPOSE_FILE) pull && docker compose -f $(COMPOSE_FILE) up -d"

# =============================================================================
# Status & Operations
# =============================================================================

status:  ## Show remote container status
 DOCKER_HOST="ssh://$(REMOTE_USER)@$(REMOTE_HOST)" docker compose -f $(COMPOSE_FILE) ps

logs:  ## Tail remote logs
 DOCKER_HOST="ssh://$(REMOTE_USER)@$(REMOTE_HOST)" docker compose -f $(COMPOSE_FILE) logs -f --tail=100

rollback:  ## Rollback to previous image
 @echo "Pull the previous image tag and restart:"
 @echo "  make -f Makefile.deploy deploy VERSION={previous_tag}"
```

## Required Variables

```makefile
REMOTE_HOST ?= deploy.example.com
REMOTE_USER ?= deploy
COMPOSE_FILE := docker-compose.prod.yml
```

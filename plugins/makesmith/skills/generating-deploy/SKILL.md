---
name: generating-deploy
description: Use when a project needs DevOps targets for building Docker images, pushing to registries (GCR/ECR/ACR), and deploying via Helm, kubectl, or Docker Compose
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

Read `references/common-template.makefile` for the base structure (header, build, push, utilities).

Customize the template:

- Replace `{project_name}` with detected project name
- Include only push targets for user-selected registries (remove others)
- Include only registry variables for selected registries
- Insert deployment targets from the loaded reference file (step 5)
- For one-to-many deployments, use the multi-deployment section from the reference

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

## Registry Login

| Registry | Command |
|----------|---------|
| GCR | `gcloud auth configure-docker gcr.io --quiet` |
| ECR | `aws ecr get-login-password --region REGION \| docker login --username AWS --password-stdin ACCOUNT.dkr.ecr.REGION.amazonaws.com` |
| ACR | `az acr login --name REGISTRY` |
| DockerHub | `docker login` |

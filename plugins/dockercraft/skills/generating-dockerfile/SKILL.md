---
name: generating-dockerfile
description: Generate optimized Dockerfile and .dockerignore for any project. Detects project language(s) and applies appropriate build strategies.
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
---

# Generate Dockerfile (Language-Aware)

Generate optimized Dockerfile and .dockerignore by detecting project language(s) and applying best practices.

## Universal Docker Standards

These apply to ALL languages:

- **Multi-stage builds** - Separate builder and runtime stages
- **Minimal runtime image** - Only production dependencies
- **Non-root user** - Security best practice
- **Entry point detection** - Detect from project context
- **Cache optimization** - Layer ordering for fast rebuilds
- **Reproducible builds** - Locked dependencies

## Workflow

### 1. Detect Project Language(s)

```text
Glob: pyproject.toml, requirements.txt, package.json, go.mod, Cargo.toml, pom.xml, build.gradle, Gemfile
```

| File Found | Language | Reference File |
|------------|----------|----------------|
| `pyproject.toml` or `requirements.txt` | Python | `references/python.md` |
| `package.json` | Node.js/React | `references/nodejs.md` |
| `go.mod` | Go | `references/go.md` |
| `Cargo.toml` | Rust | `references/rust.md` |
| `pom.xml` or `build.gradle` | Java | `references/java.md` |

### 2. Single Language Project

If ONE language detected:

1. Read the corresponding language reference file
2. Follow its specific Dockerfile template and patterns
3. Generate Dockerfile and .dockerignore

### 3. Multi-Language Project

If MULTIPLE languages detected (e.g., Python backend + React frontend):

1. Read ALL relevant language reference files
2. Present user with options via AskUserQuestion:

```text
Detected languages: Python, Node.js (React)

How should we containerize?

○ Monorepo (single Dockerfile with multi-stage for both)
○ Separate containers (Dockerfile.backend, Dockerfile.frontend)
○ Backend only (Python)
○ Frontend only (Node.js/React)
```

1. For monorepo approach, read `references/multi-language.md` for merging strategies
2. Generate appropriate Dockerfile(s)

### 4. No Language Detected

If no language files found:

1. Ask user via AskUserQuestion which language/framework they're using
2. Proceed with selected language reference

### 5. Generate .dockerignore

Universal .dockerignore (language-specific additions from reference files):

```dockerignore
# =============================================================================
# .dockerignore - Exclude from Docker build context
# =============================================================================

# Git
.git/
.gitignore
.gitattributes

# IDE
.idea/
.vscode/
*.swp
*.swo
*~

# Local configuration (secrets)
*.env
*.env.*
!*.env.example
local.*.yaml

# Development files
Makefile.local
Makefile.deploy
tests/
docs/
*.md
!README.md

# Docker (prevent recursive context)
Dockerfile*
docker-compose*.yml
.dockerignore

# Language-specific exclusions added below
{language_specific_ignores}
```

### 6. Report

```text
Created Docker configuration:

Language(s) detected: {languages}
Reference(s) used: {reference_files}

Dockerfile
  - Multi-stage build (builder + runtime)
  - Dependency manager: {dep_manager}
  - Non-root user configured
  - Entry point: {entry_point}

.dockerignore
  - Universal exclusions + {language}-specific

Commands:
  docker build -t myapp .           # Build image
  docker run -p 8000:8000 myapp     # Run container

Next steps:
  - Use dockercraft:compose to generate docker-compose.yml
```

## Language Reference Files

Read these based on detected language:

- `references/python.md` - Python with uv, multi-stage, FastAPI/Flask patterns
- `references/nodejs.md` - Node.js with npm/yarn/pnpm, React/Next.js patterns
- `references/go.md` - Go with modules, static binary builds
- `references/rust.md` - Rust with cargo, musl builds
- `references/java.md` - Java with Maven/Gradle, JRE runtime
- `references/multi-language.md` - Strategies for combining languages

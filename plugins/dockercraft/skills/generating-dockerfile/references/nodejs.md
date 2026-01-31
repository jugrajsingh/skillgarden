# Node.js Dockerfile Reference

Node.js-specific Dockerfile patterns for backend APIs, React/Next.js frontends, and full-stack applications.

## Dependency Manager Detection

Check `package.json` and lockfiles:

| Lockfile Found | Package Manager |
|----------------|-----------------|
| `pnpm-lock.yaml` | pnpm (preferred) |
| `yarn.lock` | yarn |
| `package-lock.json` | npm |
| `bun.lockb` | bun |

## Project Type Detection

| Check | Type |
|-------|------|
| `next.config.*` | Next.js |
| `vite.config.*` | Vite (React/Vue) |
| `angular.json` | Angular |
| `svelte.config.*` | SvelteKit |
| `remix.config.*` | Remix |
| `nuxt.config.*` | Nuxt |
| None of above | Plain Node.js API |

## Entry Point Detection

| Check | CMD Generated |
|-------|---------------|
| `package.json` scripts.start | `CMD ["npm", "start"]` |
| `package.json` main field | `CMD ["node", "{main}"]` |
| `server.js` exists | `CMD ["node", "server.js"]` |
| `index.js` exists | `CMD ["node", "index.js"]` |
| `dist/index.js` (built) | `CMD ["node", "dist/index.js"]` |

## Dockerfile Templates

### Node.js API (pnpm)

```dockerfile
# syntax=docker/dockerfile:1

# =============================================================================
# Stage 1: Install dependencies
# =============================================================================
FROM node:20-slim AS deps

WORKDIR /app

# Enable corepack for pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate

# Install dependencies (cached layer)
COPY package.json pnpm-lock.yaml ./
RUN --mount=type=cache,target=/root/.local/share/pnpm/store \
    pnpm install --frozen-lockfile --prod

# =============================================================================
# Stage 2: Build (if needed)
# =============================================================================
FROM node:20-slim AS builder

WORKDIR /app

RUN corepack enable && corepack prepare pnpm@latest --activate

COPY package.json pnpm-lock.yaml ./
RUN --mount=type=cache,target=/root/.local/share/pnpm/store \
    pnpm install --frozen-lockfile

COPY . .
RUN pnpm build

# =============================================================================
# Stage 3: Runtime
# =============================================================================
FROM node:20-slim AS runtime

WORKDIR /app

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser

# Copy production dependencies
COPY --from=deps /app/node_modules ./node_modules

# Copy built application
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./

ENV NODE_ENV=production

USER appuser

EXPOSE {port}

CMD ["node", "dist/index.js"]
```

### Next.js (Standalone)

```dockerfile
# syntax=docker/dockerfile:1

# =============================================================================
# Stage 1: Dependencies
# =============================================================================
FROM node:20-alpine AS deps

WORKDIR /app

RUN corepack enable

COPY package.json pnpm-lock.yaml* yarn.lock* package-lock.json* ./
RUN \
    if [ -f pnpm-lock.yaml ]; then corepack prepare pnpm@latest --activate && pnpm install --frozen-lockfile; \
    elif [ -f yarn.lock ]; then yarn install --frozen-lockfile; \
    elif [ -f package-lock.json ]; then npm ci; \
    else npm install; \
    fi

# =============================================================================
# Stage 2: Build
# =============================================================================
FROM node:20-alpine AS builder

WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Build Next.js with standalone output
ENV NEXT_TELEMETRY_DISABLED=1
RUN \
    if [ -f pnpm-lock.yaml ]; then corepack enable && pnpm build; \
    elif [ -f yarn.lock ]; then yarn build; \
    else npm run build; \
    fi

# =============================================================================
# Stage 3: Runtime (standalone)
# =============================================================================
FROM node:20-alpine AS runtime

WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Copy standalone build
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "server.js"]
```

**Note:** Requires `output: 'standalone'` in `next.config.js`

### React/Vite (Static Build)

```dockerfile
# syntax=docker/dockerfile:1

# =============================================================================
# Stage 1: Build
# =============================================================================
FROM node:20-alpine AS builder

WORKDIR /app

RUN corepack enable

COPY package.json pnpm-lock.yaml* yarn.lock* package-lock.json* ./
RUN \
    if [ -f pnpm-lock.yaml ]; then corepack prepare pnpm@latest --activate && pnpm install --frozen-lockfile; \
    elif [ -f yarn.lock ]; then yarn install --frozen-lockfile; \
    else npm ci; \
    fi

COPY . .
RUN \
    if [ -f pnpm-lock.yaml ]; then pnpm build; \
    elif [ -f yarn.lock ]; then yarn build; \
    else npm run build; \
    fi

# =============================================================================
# Stage 2: Serve with nginx
# =============================================================================
FROM nginx:alpine AS runtime

# Copy built assets
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx config for SPA routing
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

**nginx.conf for SPA:**

```nginx
server {
    listen 80;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://api:8000;
    }
}
```

## .dockerignore Additions

Add these Node.js-specific exclusions:

```dockerignore
# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.pnpm-debug.log*

# Build outputs
dist/
build/
.next/
.nuxt/
.output/
.svelte-kit/

# Testing
coverage/
.nyc_output/

# TypeScript
*.tsbuildinfo

# Environment
.env*
!.env.example

# Misc
.turbo/
.vercel/
.cache/
```

## Dependency Detection for Services

Scan `package.json` dependencies for:

| Dependency | Service Hint |
|------------|--------------|
| `pg`, `postgres`, `@prisma/client` (postgres) | postgres |
| `redis`, `ioredis`, `bull`, `bullmq` | redis |
| `@elastic/elasticsearch` | elasticsearch |
| `mongoose`, `mongodb` | mongodb |
| `amqplib`, `@nestjs/microservices` (rabbitmq) | rabbitmq |
| `kafkajs`, `@nestjs/microservices` (kafka) | kafka |
| `mysql`, `mysql2` | mysql |
| `@aws-sdk/*`, `aws-sdk` | localstack |

## Framework-Specific Ports

| Framework | Default Port |
|-----------|--------------|
| Express/Fastify/Nest | 3000 |
| Next.js | 3000 |
| Vite dev | 5173 |
| React (nginx) | 80 |
| Angular | 4200 |

## Image Size Optimization

- Use `node:20-slim` or `node:20-alpine` for runtime
- Multi-stage separates build tools from runtime
- `--frozen-lockfile` ensures reproducibility
- Cache mounts for package manager stores

Typical sizes:

- Build stage: ~800MB (includes dev deps, build tools)
- Runtime (API): ~200MB (node + prod deps)
- Runtime (static/nginx): ~30MB

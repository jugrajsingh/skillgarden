# Node.js Makefile Audit Checks

Language-specific checks for Node.js/TypeScript projects.

## Detection

Load this reference when any of these are found:

```text
Glob: package.json, package-lock.json, yarn.lock, pnpm-lock.yaml
```

## Package Manager Detection

| Lock File | Manager | Run Command |
|-----------|---------|-------------|
| `package-lock.json` | npm | `npx` or `npm run` |
| `yarn.lock` | yarn | `yarn` |
| `pnpm-lock.yaml` | pnpm | `pnpm exec` or `pnpm run` |

## Makefile.local Checks

### Command Runner

| Check | Pass Criteria | Priority |
|-------|---------------|----------|
| Correct runner | Commands use `npx`/`npm run`/`yarn`/`pnpm run` — not global installs | High |
| No global installs | No `npm install -g` in recipes | High |
| Lock file respected | `npm ci` or `--frozen-lockfile` for reproducible installs | Medium |

### Required Variables

| Check | Pass Criteria | Priority |
|-------|---------------|----------|
| NODE_ENV set | `NODE_ENV` used appropriately in run targets | Medium |

### Required Targets

| Target | Expected Command | Priority |
|--------|-----------------|----------|
| `install` | `npm ci` or `yarn install --frozen-lockfile` or `pnpm install --frozen-lockfile` | High |
| `dev` | `npm run dev` or equivalent | Medium |
| `build` | `npm run build` or equivalent | High |
| `test` | `npm test` or `npx jest`/`npx vitest` | High |
| `lint` | `npx eslint .` or `npx biome check .` | High |
| `format` | `npx prettier --write .` or `npx biome format .` | Medium |
| `type-check` | `npx tsc --noEmit` | Medium |
| `clean` | Remove `node_modules/`, `dist/`, `.next/`, build artifacts | Medium |

### Anti-Patterns

| Pattern | Issue | Fix |
|---------|-------|-----|
| `node script.js` without runner | Bypasses package.json scripts | Use `npm run` or `npx` |
| `npm install` in CI | Non-deterministic | Use `npm ci` |
| Global tool installs | Not reproducible | Use `npx` or dev dependency |
| `rm -rf node_modules && npm install` as clean | Slow, wasteful | Separate `clean` and `install` targets |

## Makefile.deploy Checks

### Node-Specific Deploy Patterns

| Check | Pass Criteria | Priority |
|-------|---------------|----------|
| No devDependencies in image | `npm ci --production` or `--omit=dev` in Dockerfile | Medium |
| node_modules in .dockerignore | `.dockerignore` should exclude `node_modules/` | Medium |
| Multi-stage build | Builder stage for `npm run build`, runtime copies only dist | Low |

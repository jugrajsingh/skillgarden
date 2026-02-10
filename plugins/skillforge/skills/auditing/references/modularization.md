# Reference File Modularization

## Core Principle

Reference files reduce token cost by loading content conditionally. Extract to a reference file only when the content is NOT always needed — it must be gated by a detection or user choice.

## When to Extract

| Signal | Extract? | Reason |
|--------|----------|--------|
| Content varies by detected language | Yes | Only load the detected language |
| Content varies by user choice | Yes | Only load the chosen option |
| Content is a catalog of options | Yes | Only load confirmed selections |
| Content is always needed | No | Extraction adds indirection without saving tokens |
| Content is short (< 30 lines) | No | Overhead of a separate file exceeds the benefit |

## Reference File Patterns

### Pattern 1: Language-Specific References

When a skill behaves differently per language/ecosystem. The skill detects the language, then loads only the matching reference.

**Structure:**

```text
skills/generating-dockerfile/
├── SKILL.md                    # Universal workflow + detection table
└── references/
    ├── python.md               # Python-specific Dockerfile patterns
    ├── nodejs.md               # Node.js-specific patterns
    ├── go.md                   # Go-specific patterns
    └── rust.md                 # Rust-specific patterns
```

**SKILL.md pattern:**

```markdown
| File Found | Language | Reference File |
|------------|----------|----------------|
| pyproject.toml | Python | references/python.md |
| package.json | Node.js | references/nodejs.md |
```

**Examples:**

- `dockercraft:generating-dockerfile` — Dockerfile templates per language
- `makesmith:auditing` — Makefile checks per language (uv vs npm vs go)

### Pattern 2: Service Catalog References

When a skill composes output from a set of independently selectable items. Each item is a self-contained reference file loaded only if the user confirms it.

**Structure:**

```text
skills/generating-compose/
├── SKILL.md                    # Detection + composition workflow
└── references/
    ├── postgres.md             # PostgreSQL service definition
    ├── redis.md                # Redis service definition
    ├── kafka.md                # Kafka service definition
    └── localstack.md           # LocalStack service definition
```

**SKILL.md pattern:**

```markdown
### 3. Detect Services from Dependencies

| Dependency Pattern | Suggested Service | Reference File |
|-------------------|-------------------|----------------|
| postgres, asyncpg | postgres | references/postgres.md |
| redis, ioredis | redis | references/redis.md |

### 5. Load Service References

Read ONLY the reference files for user-confirmed services.
```

**Examples:**

- `dockercraft:generating-compose` — 9 service definitions loaded per user selection

### Pattern 3: Deployment Method References

When a skill supports mutually exclusive strategies. User picks one, only that reference loads.

**Structure:**

```text
skills/generating-deploy/
├── SKILL.md                    # Common targets + strategy selection
└── references/
    ├── helm.md                 # Helm deployment targets
    ├── kubectl.md              # kubectl deployment targets
    └── compose.md              # Docker Compose over SSH targets
```

**SKILL.md pattern:**

```markdown
### 5. Load Deployment Reference

Read ONLY the reference file matching the user's choice:

| Deployment Target | Reference File |
|-------------------|----------------|
| Helm | references/helm.md |
| kubectl | references/kubectl.md |
```

**Examples:**

- `makesmith:generating-deploy` — deployment targets per strategy choice

## Reference File Anatomy

Each reference file should be self-contained with:

1. **Title** — what it provides
2. **Detection** — how to identify when this reference applies (for catalog patterns)
3. **Content** — the actual templates, definitions, or checks
4. **Variables** — any required configuration the parent skill must provide

```markdown
# Service Name

## Detection
Dependency patterns: postgres, asyncpg, psycopg

## Service Definition
{yaml/makefile/code block}

## App Environment Variables
{env vars the app needs}
```

## Anti-Patterns

### Extracting always-needed content

If the SKILL.md always loads the reference file regardless of detection, it's not saving tokens — it's just adding indirection.

### Duplicating content across references

If multiple reference files share the same section (e.g., common health check pattern), keep the common part in SKILL.md and only put the variant part in references.

### Over-splitting

One file per tiny variation. If a reference file is < 20 lines, it probably belongs inline in the parent skill or combined with a related reference.

### Removing content for token savings alone

Never remove content that adds unique value. Only extract content that is conditionally needed. The goal is conditional loading, not information loss.

## Evaluation Checklist

For each reference file, verify:

- [ ] Content is conditionally loaded (gated by detection or user choice)
- [ ] File is self-contained (can be understood without reading SKILL.md)
- [ ] No duplication with other reference files
- [ ] File is > 20 lines (worth the overhead of a separate file)
- [ ] SKILL.md has a clear loading table mapping conditions to reference files

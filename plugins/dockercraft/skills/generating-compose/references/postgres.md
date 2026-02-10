# PostgreSQL Service

## Detection

Dependency patterns: `postgres`, `asyncpg`, `psycopg`, `psycopg2`, `pg`, `prisma` (postgres provider)

## Service Definition

```yaml
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: app
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5
```

## App Environment Variables

```yaml
- POSTGRES__HOST=postgres
- POSTGRES__PORT=5432
- POSTGRES__USER=postgres
- POSTGRES__PASSWORD=postgres
- POSTGRES__DATABASE=app
```

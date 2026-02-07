# Redis Service

## Detection

Dependency patterns: `redis`, `ioredis`, `bull`, `aioredis`

## Service Definition

```yaml
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 5
```

## App Environment Variables

```yaml
- REDIS__HOST=redis
- REDIS__PORT=6379
```

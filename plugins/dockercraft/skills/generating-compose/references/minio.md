# MinIO Service

## Detection

Dependency patterns: `minio`

## Service Definition

```yaml
  minio:
    image: minio/minio:latest
    command: server /data --console-address ":9001"
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    volumes:
      - minio_data:/data
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 5s
      timeout: 5s
      retries: 5
```

## App Environment Variables

```yaml
- MINIO__ENDPOINT=minio:9000
- MINIO__ACCESS_KEY=minioadmin
- MINIO__SECRET_KEY=minioadmin
```

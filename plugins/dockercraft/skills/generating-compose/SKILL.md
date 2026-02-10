---
name: generating-compose
description: Generate docker-compose.yml for local development. Detects services from project dependencies and configures health checks. Use for setting up Docker-based local development with databases, caches, and other services.
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
---

# Generate docker-compose.yml

Generate docker-compose.yml for local development by detecting required services from project dependencies.

## Philosophy

- **Service detection** - Scan dependencies for service hints
- **Health checks** - Reliable startup ordering
- **Volume persistence** - Data survives container restarts
- **Development-first** - Mount source code, enable debugging

## Workflow

### 1. Check for Existing Dockerfile

```text
Glob: Dockerfile, Dockerfile.*
```

If no Dockerfile found, suggest running dockercraft:dockerfile first.

### 2. Detect Project Type

```text
Glob: pyproject.toml, package.json, go.mod, Cargo.toml, pom.xml
```

### 3. Detect Services from Dependencies

Scan dependency files for service hints:

| Dependency Pattern | Suggested Service | Reference File |
|-------------------|-------------------|----------------|
| postgres, asyncpg, psycopg, pg, prisma (postgres) | postgres | `references/postgres.md` |
| redis, ioredis, bull, aioredis | redis | `references/redis.md` |
| elasticsearch, @elastic/elasticsearch | elasticsearch | `references/elasticsearch.md` |
| mongo, mongoose, pymongo, motor | mongodb | `references/mongodb.md` |
| rabbitmq, amqp, amqplib, pika, celery, kombu | rabbitmq | `references/rabbitmq.md` |
| kafka, kafkajs, confluent-kafka, aiokafka | kafka | `references/kafka.md` |
| mysql, mysql2, mysqlclient | mysql | `references/mysql.md` |
| aws, boto, boto3, aiobotocore, s3, sqs, @aws-sdk | localstack | `references/localstack.md` |
| minio | minio | `references/minio.md` |

### 4. Ask User to Confirm Services

Present multi-select via AskUserQuestion with detected services pre-selected:

```text
Detected services from dependencies:

☑ postgres (asyncpg found)
☑ redis (redis found)
☐ elasticsearch
☐ mongodb
☐ localstack (AWS)
☐ rabbitmq
☐ kafka
☐ minio

Select services for docker-compose.yml:
```

### 5. Load Service References

Read ONLY the reference files for user-confirmed services. Each reference file contains:

- Service definition (image, ports, volumes, healthcheck)
- App environment variables

### 6. Ask About App Configuration

Via AskUserQuestion:

```text
App configuration:

Port: [8000]
Environment: [local]
Mount source code? [Yes/No]
```

### 7. Generate docker-compose.yml

Compose the file using the app skeleton below plus service definitions from loaded references:

```yaml
# =============================================================================
# docker-compose.yml - Local Development
# =============================================================================
# Usage:
#   docker compose up -d        # Start all services
#   docker compose logs -f app  # Follow app logs
#   docker compose down         # Stop all services
# =============================================================================

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      - ENVIRONMENT=local
      - DEBUG=true
      {service_env_vars}
    volumes:
      - .:/app:ro
    ports:
      - "{app_port}:{app_port}"
    depends_on:
      {service_dependencies}

{service_definitions}

volumes:
  {volume_definitions}
```

### 8. depends_on with Conditions

For proper startup ordering, use health-check-based conditions:

```yaml
depends_on:
  postgres:
    condition: service_healthy
  redis:
    condition: service_healthy
```

### 9. Report

```text
Created docker-compose.yml:

App configuration:
  - Port: {port}
  - Source mounted: {yes/no}

Services ({count}):
  {service_list_with_ports}

Environment variables added:
  {env_vars}

Commands:
  docker compose up -d          # Start all services
  docker compose logs -f app    # View app logs
  docker compose ps             # List containers
  docker compose down           # Stop all services
  docker compose down -v        # Stop and remove volumes
```

## Service Reference Files

Each service is defined in its own reference file under `references/`:

- `references/postgres.md` - PostgreSQL 16 with health check
- `references/redis.md` - Redis 7 with persistence
- `references/elasticsearch.md` - Elasticsearch 8 single-node
- `references/mongodb.md` - MongoDB 7
- `references/rabbitmq.md` - RabbitMQ 3 with management UI
- `references/kafka.md` - Confluent Kafka + Zookeeper
- `references/localstack.md` - LocalStack for AWS services
- `references/minio.md` - MinIO S3-compatible storage
- `references/mysql.md` - MySQL 8

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

| Dependency Pattern | Suggested Service |
|-------------------|-------------------|
| postgres, asyncpg, psycopg, pg, prisma (postgres) | postgres |
| redis, ioredis, bull | redis |
| elasticsearch, @elastic/elasticsearch | elasticsearch |
| mongo, mongoose, pymongo | mongodb |
| rabbitmq, amqp, amqplib, pika | rabbitmq |
| kafka, kafkajs, confluent-kafka | kafka |
| mysql, mysql2, mysqlclient | mysql |
| aws, boto, s3, sqs, @aws-sdk | localstack |
| minio | minio |

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

### 5. Ask About App Configuration

Via AskUserQuestion:

```text
App configuration:

Port: [8000]
Environment: [local]
Mount source code? [Yes/No]
```

### 6. Generate docker-compose.yml

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

### 7. Report

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

## Service Definitions

### postgres

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

**App env vars:**

```yaml
- POSTGRES__HOST=postgres
- POSTGRES__PORT=5432
- POSTGRES__USER=postgres
- POSTGRES__PASSWORD=postgres
- POSTGRES__DATABASE=app
```

### redis

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

**App env vars:**

```yaml
- REDIS__HOST=redis
- REDIS__PORT=6379
```

### elasticsearch

```yaml
  elasticsearch:
    image: elasticsearch:8.11.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ports:
      - "9200:9200"
    volumes:
      - es_data:/usr/share/elasticsearch/data
    healthcheck:
      test: ["CMD-SHELL", "curl -s http://localhost:9200/_cluster/health | grep -q '\"status\":\"green\"\\|\"status\":\"yellow\"'"]
      interval: 10s
      timeout: 5s
      retries: 10
```

**App env vars:**

```yaml
- ES__HOSTS=["http://elasticsearch:9200"]
```

### mongodb

```yaml
  mongodb:
    image: mongo:7
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
      interval: 5s
      timeout: 5s
      retries: 5
```

**App env vars:**

```yaml
- MONGO__URI=mongodb://mongodb:27017/app
```

### rabbitmq

```yaml
  rabbitmq:
    image: rabbitmq:3-management-alpine
    ports:
      - "5672:5672"
      - "15672:15672"
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "check_running"]
      interval: 5s
      timeout: 5s
      retries: 5
```

**App env vars:**

```yaml
- RABBITMQ__HOST=rabbitmq
- RABBITMQ__PORT=5672
```

### kafka

```yaml
  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
    volumes:
      - zookeeper_data:/var/lib/zookeeper/data

  kafka:
    image: confluentinc/cp-kafka:7.5.0
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:29092,PLAINTEXT_HOST://localhost:9092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
    volumes:
      - kafka_data:/var/lib/kafka/data
```

**App env vars:**

```yaml
- KAFKA__BOOTSTRAP_SERVERS=kafka:29092
```

### localstack

```yaml
  localstack:
    image: localstack/localstack:latest
    environment:
      - SERVICES=s3,sqs,sns,dynamodb
      - DEBUG=1
    ports:
      - "4566:4566"
    volumes:
      - localstack_data:/var/lib/localstack
```

**App env vars:**

```yaml
- AWS__ENDPOINT_URL=http://localstack:4566
- AWS__REGION=us-east-1
- AWS__ACCESS_KEY_ID=test
- AWS__SECRET_ACCESS_KEY=test
```

### minio

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

**App env vars:**

```yaml
- MINIO__ENDPOINT=minio:9000
- MINIO__ACCESS_KEY=minioadmin
- MINIO__SECRET_KEY=minioadmin
```

### mysql

```yaml
  mysql:
    image: mysql:8
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: app
      MYSQL_USER: app
      MYSQL_PASSWORD: app
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 5s
      timeout: 5s
      retries: 5
```

**App env vars:**

```yaml
- MYSQL__HOST=mysql
- MYSQL__PORT=3306
- MYSQL__USER=app
- MYSQL__PASSWORD=app
- MYSQL__DATABASE=app
```

## depends_on with Conditions

For proper startup ordering:

```yaml
depends_on:
  postgres:
    condition: service_healthy
  redis:
    condition: service_healthy
```

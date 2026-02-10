# RabbitMQ Service

## Detection

Dependency patterns: `rabbitmq`, `amqp`, `amqplib`, `pika`, `celery`, `kombu`

## Service Definition

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

## App Environment Variables

```yaml
- RABBITMQ__HOST=rabbitmq
- RABBITMQ__PORT=5672
```

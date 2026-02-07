# LocalStack Service

## Detection

Dependency patterns: `aws`, `boto`, `boto3`, `aiobotocore`, `s3`, `sqs`, `@aws-sdk`

## Service Definition

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

## App Environment Variables

```yaml
- AWS__ENDPOINT_URL=http://localstack:4566
- AWS__REGION=us-east-1
- AWS__ACCESS_KEY_ID=test
- AWS__SECRET_ACCESS_KEY=test
```

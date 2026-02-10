# MySQL Service

## Detection

Dependency patterns: `mysql`, `mysql2`, `mysqlclient`

## Service Definition

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

## App Environment Variables

```yaml
- MYSQL__HOST=mysql
- MYSQL__PORT=3306
- MYSQL__USER=app
- MYSQL__PASSWORD=app
- MYSQL__DATABASE=app
```

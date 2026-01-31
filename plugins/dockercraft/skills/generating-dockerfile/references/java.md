# Java Dockerfile Reference

Java-specific Dockerfile patterns for Maven and Gradle projects with JRE slim runtime.

## Build Tool Detection

| File Found | Build Tool |
|------------|-----------|
| `pom.xml` | Maven |
| `build.gradle` or `build.gradle.kts` | Gradle |
| `mvnw` | Maven Wrapper |
| `gradlew` | Gradle Wrapper |

## Entry Point Detection

| Check | CMD Generated |
|-------|---------------|
| Spring Boot with Maven | `CMD ["java", "-jar", "app.jar"]` |
| Spring Boot with Gradle | `CMD ["java", "-jar", "app.jar"]` |
| `MANIFEST.MF` Main-Class | `CMD ["java", "-jar", "app.jar"]` |
| Quarkus | `CMD ["java", "-jar", "quarkus-run.jar"]` |

## Dockerfile Templates

### Maven (Spring Boot)

```dockerfile
# syntax=docker/dockerfile:1

# =============================================================================
# Stage 1: Build
# =============================================================================
FROM eclipse-temurin:21-jdk-jammy AS builder

WORKDIR /app

# Copy Maven wrapper and POM (cached layer)
COPY mvnw pom.xml ./
COPY .mvn .mvn
RUN --mount=type=cache,target=/root/.m2 \
    chmod +x mvnw && ./mvnw dependency:go-offline -B

# Copy source and build
COPY src ./src
RUN --mount=type=cache,target=/root/.m2 \
    ./mvnw package -DskipTests -B

# =============================================================================
# Stage 2: Runtime
# =============================================================================
FROM eclipse-temurin:21-jre-jammy AS runtime

WORKDIR /app

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser

# Copy JAR from builder
COPY --from=builder /app/target/*.jar app.jar

USER appuser

EXPOSE 8080

CMD ["java", "-jar", "app.jar"]
```

### Gradle (Spring Boot)

```dockerfile
# syntax=docker/dockerfile:1

# =============================================================================
# Stage 1: Build
# =============================================================================
FROM eclipse-temurin:21-jdk-jammy AS builder

WORKDIR /app

# Copy Gradle wrapper and config (cached layer)
COPY gradlew build.gradle* settings.gradle* ./
COPY gradle gradle
RUN --mount=type=cache,target=/root/.gradle \
    chmod +x gradlew && ./gradlew dependencies --no-daemon

# Copy source and build
COPY src ./src
RUN --mount=type=cache,target=/root/.gradle \
    ./gradlew bootJar --no-daemon

# =============================================================================
# Stage 2: Runtime
# =============================================================================
FROM eclipse-temurin:21-jre-jammy AS runtime

WORKDIR /app

RUN useradd --create-home --shell /bin/bash appuser

COPY --from=builder /app/build/libs/*.jar app.jar

USER appuser

EXPOSE 8080

CMD ["java", "-jar", "app.jar"]
```

## JVM Optimization

```dockerfile
# Production JVM flags
CMD ["java", \
     "-XX:+UseContainerSupport", \
     "-XX:MaxRAMPercentage=75.0", \
     "-XX:+UseG1GC", \
     "-jar", "app.jar"]
```

## .dockerignore Additions

```dockerignore
# Java
target/
build/
.gradle/
*.class
*.jar
*.war

# IDE
.idea/
*.iml
.settings/
.classpath
.project
```

## Dependency Detection for Services

Scan `pom.xml` or `build.gradle` for:

| Dependency | Service Hint |
|------------|--------------|
| `spring-boot-starter-data-jpa` + `postgresql` | postgres |
| `spring-boot-starter-data-redis` | redis |
| `spring-data-elasticsearch` | elasticsearch |
| `spring-boot-starter-data-mongodb` | mongodb |
| `spring-boot-starter-amqp` | rabbitmq |
| `spring-kafka` | kafka |
| `mysql-connector-java` | mysql |

## Base Image Options

| Image | Size | Use Case |
|-------|------|----------|
| `eclipse-temurin:21-jre-jammy` | ~200MB | Standard JRE |
| `eclipse-temurin:21-jre-alpine` | ~150MB | Alpine-based |
| `gcr.io/distroless/java21` | ~200MB | No shell, secure |

## Image Size Optimization

Typical sizes:

- Build stage: ~800MB (JDK + Maven/Gradle + deps)
- Runtime (JRE): ~250MB (JRE + app JAR)
- Runtime (distroless): ~220MB

Tips:

- Use JRE, not JDK in runtime
- Cache Maven/Gradle downloads with mount cache
- Use layered JARs for better caching (Spring Boot)

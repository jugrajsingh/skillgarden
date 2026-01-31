# Rust Dockerfile Reference

Rust-specific Dockerfile patterns with cargo-chef for dependency caching and musl for static builds.

## Build Strategy

- **cargo-chef** - Cache compiled dependencies between builds
- **musl target** - Fully static binaries for scratch/distroless
- **Multi-stage** - Separate planner, builder, and runtime stages

## Entry Point Detection

| Check | Binary Name |
|-------|-------------|
| `Cargo.toml` package name | Package name from manifest |
| `src/main.rs` exists | Default binary |
| `src/bin/` directory | Multiple binaries |

## Dockerfile Template (with cargo-chef)

```dockerfile
# syntax=docker/dockerfile:1

# =============================================================================
# Stage 1: Prepare recipe (dependency manifest)
# =============================================================================
FROM rust:1.77-slim-bookworm AS planner

WORKDIR /app
RUN cargo install cargo-chef

COPY . .
RUN cargo chef prepare --recipe-path recipe.json

# =============================================================================
# Stage 2: Build dependencies (cached layer)
# =============================================================================
FROM rust:1.77-slim-bookworm AS builder

WORKDIR /app
RUN cargo install cargo-chef

# Install musl tools for static builds
RUN apt-get update && apt-get install -y musl-tools && rm -rf /var/lib/apt/lists/*
RUN rustup target add x86_64-unknown-linux-musl

# Cook dependencies (cached unless Cargo.toml/Cargo.lock change)
COPY --from=planner /app/recipe.json recipe.json
RUN cargo chef cook --release --target x86_64-unknown-linux-musl --recipe-path recipe.json

# Build application
COPY . .
RUN cargo build --release --target x86_64-unknown-linux-musl

# =============================================================================
# Stage 3: Runtime (scratch - zero dependencies)
# =============================================================================
FROM scratch AS runtime

# Copy CA certificates
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

# Copy statically linked binary
COPY --from=builder /app/target/x86_64-unknown-linux-musl/release/{binary_name} /{binary_name}

USER 1000:1000

EXPOSE {port}

ENTRYPOINT ["/{binary_name}"]
```

## Without cargo-chef (simpler)

```dockerfile
# syntax=docker/dockerfile:1

FROM rust:1.77-slim-bookworm AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y musl-tools && rm -rf /var/lib/apt/lists/*
RUN rustup target add x86_64-unknown-linux-musl

# Cache dependencies
COPY Cargo.toml Cargo.lock ./
RUN mkdir src && echo "fn main() {}" > src/main.rs
RUN cargo build --release --target x86_64-unknown-linux-musl
RUN rm -rf src

# Build actual application
COPY . .
RUN touch src/main.rs && cargo build --release --target x86_64-unknown-linux-musl

FROM scratch AS runtime

COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /app/target/x86_64-unknown-linux-musl/release/{binary_name} /{binary_name}

USER 1000:1000

EXPOSE {port}

ENTRYPOINT ["/{binary_name}"]
```

## .dockerignore Additions

```dockerignore
# Rust
target/
Cargo.lock.bak

# IDE
.idea/
*.iml
```

## Build Targets

| Target | Use Case | Image |
|--------|----------|-------|
| x86_64-unknown-linux-musl | Static binary, scratch | scratch |
| x86_64-unknown-linux-gnu | Dynamic binary, needs glibc | debian-slim |

## Framework-Specific Ports

| Framework | Default Port |
|-----------|--------------|
| Actix Web | 8080 |
| Axum | 3000 |
| Rocket | 8000 |
| Warp | 3030 |

## Image Size Optimization

Typical sizes:

- Build stage: ~2GB (Rust toolchain + deps)
- Runtime (scratch + musl): ~5-15MB (just the binary + certs)
- Runtime (debian-slim): ~80MB

Tips:

- Always use musl for smallest images
- cargo-chef saves significant rebuild time
- Strip binary with `--release` (includes optimizations)
- Add `strip = true` to Cargo.toml [profile.release]

---
name: browsing-patterns
description: Copy-paste ready code patterns for Python backend development. Includes Repository, Service, Middleware, Caching, Retry, Rate Limiter, Error Handling, Background Task, and Dependency Injection patterns. Use when implementing common architectural patterns or looking for production-ready code snippets.
allowed-tools:
  - Read
---

# Python Code Patterns Library

Copy-paste ready implementations for common backend patterns.

## Available Patterns

| Pattern | Use Case |
|---------|----------|
| Repository | Data access abstraction |
| Service Layer | Business logic encapsulation |
| Middleware | Request/response processing |
| Caching | Redis-based caching with decorator |
| Retry | Exponential backoff for external calls |
| Rate Limiter | Token bucket rate limiting |
| Error Handling | Structured application errors |
| Background Task | Graceful async task management |
| Dependency Injection | FastAPI DI patterns |

## Usage

Read `references/patterns.md` for complete implementations.

Each pattern includes:

- Complete, runnable code
- Type hints
- Docstrings
- Usage examples

## Quick Reference

### Repository Pattern

```python
class BaseRepository(ABC, Generic[T]):
    async def get(self, id: str) -> T | None: ...
    async def create(self, entity: T) -> T: ...
    async def list(self, limit: int = 100) -> list[T]: ...
```

### Service Result Pattern

```python
@dataclass
class ServiceResult(Generic[T]):
    success: bool
    data: T | None = None
    error: str | None = None

    @classmethod
    def ok(cls, data: T) -> "ServiceResult[T]": ...
    @classmethod
    def fail(cls, error: str) -> "ServiceResult[T]": ...
```

### Retry Decorator

```python
@retry(max_attempts=3, delay=1.0, exceptions=(ConnectionError,))
async def fetch_external_api(url: str) -> dict: ...
```

### Dependency Injection

```python
def get_user_service(
    repo: Annotated[UserRepository, Depends(get_user_repo)],
) -> UserService:
    return UserService(repo)
```

For complete implementations, read `references/patterns.md`.

# Python Code Patterns - Complete Implementations

Copy-paste ready implementations for common backend patterns. Use these as starting points.

## Table of Contents

- [Repository Pattern](#repository-pattern)
- [Service Layer Pattern](#service-layer-pattern)
- [Middleware Pattern](#middleware-pattern-fastapi)
- [Caching Pattern](#caching-pattern)
- [Retry Pattern](#retry-pattern)
- [Rate Limiter Pattern](#rate-limiter-pattern)
- [Error Handling Pattern](#error-handling-pattern)
- [Background Task Pattern](#background-task-pattern)
- [Dependency Injection Pattern](#dependency-injection-pattern)

---

## Repository Pattern

Abstract data access layer for clean separation between business logic and persistence.

```python
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    """Abstract repository for data access.

    Provides a clean interface for CRUD operations that can be
    implemented for different storage backends (SQL, NoSQL, etc.).
    """

    @abstractmethod
    async def get(self, id: str) -> T | None:
        """Get entity by ID.

        Args:
            id: The unique identifier of the entity.

        Returns:
            The entity if found, None otherwise.
        """
        ...

    @abstractmethod
    async def create(self, entity: T) -> T:
        """Create new entity.

        Args:
            entity: The entity to create.

        Returns:
            The created entity with any generated fields populated.
        """
        ...

    @abstractmethod
    async def update(self, id: str, entity: T) -> T:
        """Update existing entity.

        Args:
            id: The unique identifier of the entity.
            entity: The updated entity data.

        Returns:
            The updated entity.

        Raises:
            ValueError: If entity with given ID doesn't exist.
        """
        ...

    @abstractmethod
    async def delete(self, id: str) -> bool:
        """Delete entity by ID.

        Args:
            id: The unique identifier of the entity.

        Returns:
            True if entity was deleted, False if not found.
        """
        ...

    @abstractmethod
    async def list(self, limit: int = 100, offset: int = 0) -> list[T]:
        """List entities with pagination.

        Args:
            limit: Maximum number of entities to return.
            offset: Number of entities to skip.

        Returns:
            List of entities.
        """
        ...


class SQLAlchemyRepository(BaseRepository[T]):
    """SQLAlchemy implementation of BaseRepository.

    Example:
        ```python
        class UserRepository(SQLAlchemyRepository[User]):
            def __init__(self, session: AsyncSession):
                super().__init__(session, User)

            async def get_by_email(self, email: str) -> User | None:
                result = await self.session.execute(
                    select(User).where(User.email == email)
                )
                return result.scalar_one_or_none()
        ```
    """

    def __init__(self, session: AsyncSession, model: type[T]):
        """Initialize repository with session and model.

        Args:
            session: SQLAlchemy async session.
            model: The SQLAlchemy model class.
        """
        self.session = session
        self.model = model

    async def get(self, id: str) -> T | None:
        return await self.session.get(self.model, id)

    async def create(self, entity: T) -> T:
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def update(self, id: str, entity: T) -> T:
        existing = await self.get(id)
        if not existing:
            raise ValueError(f"{self.model.__name__} with id {id} not found")

        for key, value in entity.__dict__.items():
            if not key.startswith("_"):
                setattr(existing, key, value)

        await self.session.commit()
        await self.session.refresh(existing)
        return existing

    async def delete(self, id: str) -> bool:
        entity = await self.get(id)
        if not entity:
            return False
        await self.session.delete(entity)
        await self.session.commit()
        return True

    async def list(self, limit: int = 100, offset: int = 0) -> list[T]:
        result = await self.session.execute(
            select(self.model).limit(limit).offset(offset)
        )
        return list(result.scalars().all())
```

---

## Service Layer Pattern

Encapsulate business logic with clear result types.

```python
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class ServiceResult(Generic[T]):
    """Standard service response wrapper.

    Provides a consistent way to return success/failure from service methods
    without raising exceptions for expected business logic failures.

    Example:
        ```python
        result = await user_service.create_user(data)
        if result.success:
            return result.data
        else:
            raise HTTPException(400, result.error)
        ```
    """
    success: bool
    data: T | None = None
    error: str | None = None

    @classmethod
    def ok(cls, data: T) -> "ServiceResult[T]":
        """Create successful result.

        Args:
            data: The result data.

        Returns:
            ServiceResult with success=True and data populated.
        """
        return cls(success=True, data=data)

    @classmethod
    def fail(cls, error: str) -> "ServiceResult[T]":
        """Create failed result.

        Args:
            error: The error message.

        Returns:
            ServiceResult with success=False and error populated.
        """
        return cls(success=False, error=error)


class UserService:
    """Business logic for user operations.

    Encapsulates all user-related business rules and orchestrates
    interactions between repositories and external services.
    """

    def __init__(self, repo: "UserRepository", notifier: "EmailNotifier"):
        """Initialize service with dependencies.

        Args:
            repo: User repository for data access.
            notifier: Email notifier for sending notifications.
        """
        self.repo = repo
        self.notifier = notifier

    async def create_user(self, data: "CreateUserRequest") -> ServiceResult["User"]:
        """Create a new user with validation.

        Args:
            data: User creation request data.

        Returns:
            ServiceResult containing the created user or error message.
        """
        # Validation
        if await self.repo.get_by_email(data.email):
            return ServiceResult.fail("Email already exists")

        # Create
        user = User(email=data.email, name=data.name)
        created = await self.repo.create(user)

        # Side effects
        await self.notifier.send_welcome(created)

        return ServiceResult.ok(created)

    async def deactivate_user(self, user_id: str) -> ServiceResult[bool]:
        """Deactivate a user account.

        Args:
            user_id: The user's unique identifier.

        Returns:
            ServiceResult indicating success or failure.
        """
        user = await self.repo.get(user_id)
        if not user:
            return ServiceResult.fail("User not found")

        if not user.is_active:
            return ServiceResult.fail("User already deactivated")

        user.is_active = False
        await self.repo.update(user_id, user)

        return ServiceResult.ok(True)
```

---

## Middleware Pattern (FastAPI)

Request/response processing for cross-cutting concerns.

```python
from time import perf_counter
from uuid import uuid4

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class TimingMiddleware(BaseHTTPMiddleware):
    """Add request timing headers.

    Adds X-Response-Time header to all responses with the
    request processing duration in seconds.
    """

    async def dispatch(self, request: Request, call_next):
        start = perf_counter()
        response = await call_next(request)
        duration = perf_counter() - start
        response.headers["X-Response-Time"] = f"{duration:.3f}s"
        return response


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Add unique request ID for tracing.

    Extracts X-Request-ID from incoming request or generates a new one.
    Makes the ID available via request.state.request_id and adds it
    to the response headers.
    """

    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid4()))
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


class LoggingMiddleware(BaseHTTPMiddleware):
    """Log all requests with timing and status.

    Logs request method, path, status code, and duration for
    observability and debugging.
    """

    async def dispatch(self, request: Request, call_next):
        from utils.log import get_logger

        logger = get_logger(__name__)
        start = perf_counter()

        response = await call_next(request)

        duration = perf_counter() - start
        logger.info(
            "Request completed",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": round(duration * 1000, 2),
                "request_id": getattr(request.state, "request_id", None),
            },
        )

        return response


# Usage in FastAPI app
# app.add_middleware(RequestIDMiddleware)
# app.add_middleware(TimingMiddleware)
# app.add_middleware(LoggingMiddleware)
```

---

## Caching Pattern

Redis-based caching with decorator support.

```python
import json
from functools import wraps
from typing import Any, Callable

from redis.asyncio import Redis


class CacheService:
    """Redis-based caching service.

    Provides async get/set/delete operations with JSON serialization
    and configurable TTL.

    Example:
        ```python
        cache = CacheService(redis_client)
        await cache.set("user:123", {"name": "John"}, ttl=600)
        user = await cache.get("user:123")
        ```
    """

    def __init__(self, redis: Redis, default_ttl: int = 300):
        """Initialize cache service.

        Args:
            redis: Async Redis client instance.
            default_ttl: Default time-to-live in seconds.
        """
        self.redis = redis
        self.default_ttl = default_ttl

    async def get(self, key: str) -> dict | None:
        """Get cached value by key.

        Args:
            key: Cache key.

        Returns:
            Cached dict value or None if not found.
        """
        data = await self.redis.get(key)
        return json.loads(data) if data else None

    async def set(self, key: str, value: dict, ttl: int | None = None) -> None:
        """Set cached value with TTL.

        Args:
            key: Cache key.
            value: Dict value to cache.
            ttl: Time-to-live in seconds, uses default if not provided.
        """
        await self.redis.set(key, json.dumps(value), ex=ttl or self.default_ttl)

    async def delete(self, key: str) -> None:
        """Delete cached value.

        Args:
            key: Cache key to delete.
        """
        await self.redis.delete(key)

    async def invalidate_pattern(self, pattern: str) -> int:
        """Delete all keys matching pattern.

        Args:
            pattern: Glob pattern to match keys (e.g., "user:*").

        Returns:
            Number of keys deleted.
        """
        keys = await self.redis.keys(pattern)
        if keys:
            return await self.redis.delete(*keys)
        return 0


def cached(key_prefix: str, ttl: int = 300):
    """Decorator for caching function results.

    Caches the return value of async methods using a key built from
    the prefix and function arguments.

    Args:
        key_prefix: Prefix for cache keys.
        ttl: Time-to-live in seconds.

    Example:
        ```python
        class ProductService:
            def __init__(self, cache: CacheService):
                self.cache = cache

            @cached("product", ttl=600)
            async def get_product(self, product_id: str) -> dict:
                # This will be cached as "product:123"
                return await self.repo.get(product_id)
        ```
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(self, *args, **kwargs) -> Any:
            cache_key = f"{key_prefix}:{':'.join(str(a) for a in args)}"

            cached_value = await self.cache.get(cache_key)
            if cached_value is not None:
                return cached_value

            result = await func(self, *args, **kwargs)
            await self.cache.set(cache_key, result, ttl)
            return result
        return wrapper
    return decorator
```

---

## Retry Pattern

Exponential backoff for resilient external calls.

```python
import asyncio
from functools import wraps
from typing import Callable, TypeVar

import httpx

from utils.log import get_logger

logger = get_logger(__name__)
T = TypeVar("T")


def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (Exception,),
):
    """Retry decorator with exponential backoff.

    Automatically retries failed async function calls with configurable
    delays and backoff multiplier.

    Args:
        max_attempts: Maximum number of attempts before giving up.
        delay: Initial delay between retries in seconds.
        backoff: Multiplier for delay after each attempt.
        exceptions: Tuple of exception types to catch and retry.

    Example:
        ```python
        @retry(max_attempts=3, delay=1.0, exceptions=(ConnectionError,))
        async def fetch_data(url: str) -> dict:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                return response.json()
        ```
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            last_exception = None
            current_delay = delay

            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        logger.warning(
                            "Retry attempt failed",
                            extra={
                                "function": func.__name__,
                                "attempt": attempt + 1,
                                "max_attempts": max_attempts,
                                "delay": current_delay,
                                "error": str(e),
                            },
                        )
                        await asyncio.sleep(current_delay)
                        current_delay *= backoff

            raise last_exception
        return wrapper
    return decorator


# Usage examples

@retry(max_attempts=3, delay=1.0, exceptions=(ConnectionError, TimeoutError))
async def fetch_external_api(url: str) -> dict:
    """Fetch JSON from external API with retries."""
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=10.0)
        response.raise_for_status()
        return response.json()


@retry(max_attempts=5, delay=0.5, backoff=1.5, exceptions=(httpx.HTTPStatusError,))
async def post_with_retry(url: str, data: dict) -> dict:
    """POST data to API with retries on HTTP errors."""
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, timeout=30.0)
        response.raise_for_status()
        return response.json()
```

---

## Rate Limiter Pattern

Token bucket algorithm for rate limiting.

```python
import asyncio
from collections import defaultdict
from time import time


class RateLimiter:
    """Token bucket rate limiter.

    Implements token bucket algorithm for rate limiting concurrent
    operations. Tokens are replenished at a constant rate.

    Example:
        ```python
        limiter = RateLimiter(requests_per_second=10.0)

        async def make_api_call():
            await limiter.wait("api")  # Blocks if rate exceeded
            return await client.get(url)
        ```
    """

    def __init__(self, requests_per_second: float = 10.0):
        """Initialize rate limiter.

        Args:
            requests_per_second: Maximum requests allowed per second.
        """
        self.rate = requests_per_second
        self.tokens: dict[str, float] = defaultdict(lambda: requests_per_second)
        self.last_update: dict[str, float] = defaultdict(time)
        self._lock = asyncio.Lock()

    async def acquire(self, key: str = "default") -> bool:
        """Try to acquire a token without blocking.

        Args:
            key: Bucket key for per-resource rate limiting.

        Returns:
            True if token acquired, False if rate limit exceeded.
        """
        async with self._lock:
            now = time()
            elapsed = now - self.last_update[key]
            self.tokens[key] = min(self.rate, self.tokens[key] + elapsed * self.rate)
            self.last_update[key] = now

            if self.tokens[key] >= 1.0:
                self.tokens[key] -= 1.0
                return True
            return False

    async def wait(self, key: str = "default") -> None:
        """Wait until a token is available.

        Args:
            key: Bucket key for per-resource rate limiting.
        """
        while not await self.acquire(key):
            await asyncio.sleep(0.1)

    def get_remaining(self, key: str = "default") -> float:
        """Get remaining tokens for a key.

        Args:
            key: Bucket key.

        Returns:
            Number of remaining tokens (approximate).
        """
        now = time()
        elapsed = now - self.last_update.get(key, now)
        tokens = self.tokens.get(key, self.rate)
        return min(self.rate, tokens + elapsed * self.rate)


class SlidingWindowRateLimiter:
    """Sliding window rate limiter for more precise control.

    Uses Redis sorted sets for distributed rate limiting across
    multiple service instances.
    """

    def __init__(self, redis: "Redis", window_seconds: int = 60, max_requests: int = 100):
        """Initialize sliding window limiter.

        Args:
            redis: Async Redis client.
            window_seconds: Time window size in seconds.
            max_requests: Maximum requests allowed per window.
        """
        self.redis = redis
        self.window_seconds = window_seconds
        self.max_requests = max_requests

    async def is_allowed(self, key: str) -> bool:
        """Check if request is allowed and record it.

        Args:
            key: Unique identifier (e.g., user_id, ip_address).

        Returns:
            True if request allowed, False if rate limited.
        """
        now = time()
        window_start = now - self.window_seconds
        redis_key = f"ratelimit:{key}"

        async with self.redis.pipeline(transaction=True) as pipe:
            # Remove old entries
            await pipe.zremrangebyscore(redis_key, 0, window_start)
            # Count entries in window
            await pipe.zcard(redis_key)
            # Add current request
            await pipe.zadd(redis_key, {str(now): now})
            # Set expiry
            await pipe.expire(redis_key, self.window_seconds)

            results = await pipe.execute()
            count = results[1]

        return count < self.max_requests
```

---

## Error Handling Pattern

Structured application errors with FastAPI integration.

```python
from dataclasses import dataclass
from enum import Enum
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class ErrorCode(Enum):
    """Application error codes mapped to HTTP status codes."""
    NOT_FOUND = "NOT_FOUND"
    VALIDATION = "VALIDATION"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    CONFLICT = "CONFLICT"
    RATE_LIMITED = "RATE_LIMITED"
    INTERNAL = "INTERNAL"


@dataclass
class AppError(Exception):
    """Application-level error with code and details.

    Use for expected errors in business logic. Unexpected errors
    should still raise standard exceptions.

    Example:
        ```python
        async def get_user(user_id: str) -> User:
            user = await repo.get(user_id)
            if not user:
                raise AppError(
                    code=ErrorCode.NOT_FOUND,
                    message="User not found",
                    details={"user_id": user_id},
                )
            return user
        ```
    """
    code: ErrorCode
    message: str
    details: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-serializable dict."""
        return {
            "code": self.code.value,
            "message": self.message,
            "details": self.details,
        }


# HTTP status code mapping
ERROR_STATUS_MAP = {
    ErrorCode.NOT_FOUND: 404,
    ErrorCode.VALIDATION: 400,
    ErrorCode.UNAUTHORIZED: 401,
    ErrorCode.FORBIDDEN: 403,
    ErrorCode.CONFLICT: 409,
    ErrorCode.RATE_LIMITED: 429,
    ErrorCode.INTERNAL: 500,
}


def setup_error_handlers(app: FastAPI) -> None:
    """Register error handlers on FastAPI app.

    Args:
        app: FastAPI application instance.
    """
    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(
            status_code=ERROR_STATUS_MAP.get(exc.code, 500),
            content=exc.to_dict(),
        )

    @app.exception_handler(Exception)
    async def unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:
        from utils.log import get_logger

        logger = get_logger(__name__)
        logger.exception(
            "Unhandled exception",
            extra={"path": request.url.path, "method": request.method},
        )

        return JSONResponse(
            status_code=500,
            content={
                "code": ErrorCode.INTERNAL.value,
                "message": "An unexpected error occurred",
                "details": None,
            },
        )


# Convenience functions for common errors

def not_found(resource: str, identifier: Any) -> AppError:
    """Create NOT_FOUND error."""
    return AppError(
        code=ErrorCode.NOT_FOUND,
        message=f"{resource} not found",
        details={"identifier": str(identifier)},
    )


def validation_error(message: str, field: str | None = None) -> AppError:
    """Create VALIDATION error."""
    details = {"field": field} if field else None
    return AppError(code=ErrorCode.VALIDATION, message=message, details=details)


def unauthorized(message: str = "Authentication required") -> AppError:
    """Create UNAUTHORIZED error."""
    return AppError(code=ErrorCode.UNAUTHORIZED, message=message)
```

---

## Background Task Pattern

Graceful async task management with proper shutdown.

```python
import asyncio
from abc import ABC, abstractmethod
from typing import Any, Callable

from utils.log import get_logger

logger = get_logger(__name__)


class BackgroundTask(ABC):
    """Base class for background tasks.

    Provides lifecycle management with graceful shutdown support.
    Subclass and implement the run() method.

    Example:
        ```python
        class MetricsReporter(BackgroundTask):
            def __init__(self, interval: float = 60.0):
                super().__init__()
                self.interval = interval

            async def run(self) -> None:
                await self.collect_and_report_metrics()
                await asyncio.sleep(self.interval)
        ```
    """

    def __init__(self):
        self.terminate = False
        self._task: asyncio.Task | None = None

    @abstractmethod
    async def run(self) -> None:
        """Main task logic - override this.

        Called repeatedly until terminate is True.
        """
        ...

    async def start(self) -> None:
        """Start the background task."""
        self._task = asyncio.create_task(self._loop())
        logger.info("Background task started", extra={"task": self.__class__.__name__})

    async def stop(self, timeout: float = 10.0) -> None:
        """Stop the background task gracefully.

        Args:
            timeout: Maximum time to wait for task to finish.
        """
        self.terminate = True
        if self._task:
            try:
                await asyncio.wait_for(self._task, timeout=timeout)
            except asyncio.TimeoutError:
                logger.warning(
                    "Background task did not finish in time",
                    extra={"task": self.__class__.__name__},
                )
                self._task.cancel()
        logger.info("Background task stopped", extra={"task": self.__class__.__name__})

    async def _loop(self) -> None:
        """Internal run loop with error handling."""
        while not self.terminate:
            try:
                await self.run()
            except asyncio.CancelledError:
                break
            except Exception:
                logger.exception(
                    "Background task error",
                    extra={"task": self.__class__.__name__},
                )
                await asyncio.sleep(1.0)  # Prevent tight error loop


class QueueProcessor(BackgroundTask):
    """Process messages from a queue.

    Generic queue processor that receives batches of messages
    and processes them concurrently.

    Example:
        ```python
        processor = QueueProcessor(
            queue=sqs_queue,
            handler=process_message,
            batch_size=10,
        )
        await processor.start()
        ```
    """

    def __init__(
        self,
        queue: "Queue",
        handler: Callable[[Any], Any],
        batch_size: int = 10,
    ):
        """Initialize queue processor.

        Args:
            queue: Queue to receive messages from.
            handler: Async function to process each message.
            batch_size: Maximum messages per batch.
        """
        super().__init__()
        self.queue = queue
        self.handler = handler
        self.batch_size = batch_size

    async def run(self) -> None:
        """Receive and process a batch of messages."""
        messages = await self.queue.receive(max_messages=self.batch_size)

        if not messages:
            await asyncio.sleep(1.0)  # Avoid spinning on empty queue
            return

        results = await asyncio.gather(
            *[self._process_message(m) for m in messages],
            return_exceptions=True,
        )

        # Log any failures
        for msg, result in zip(messages, results):
            if isinstance(result, Exception):
                logger.exception(
                    "Failed to process message",
                    extra={"message_id": getattr(msg, "id", None)},
                )

    async def _process_message(self, message: Any) -> Any:
        """Process single message with error handling."""
        try:
            return await self.handler(message)
        finally:
            # Acknowledge message after processing
            await self.queue.acknowledge(message)


class TaskManager:
    """Manage multiple background tasks with graceful shutdown.

    Example:
        ```python
        manager = TaskManager()
        manager.add(QueueProcessor(queue, handler))
        manager.add(MetricsReporter())

        await manager.start_all()
        # ... application runs ...
        await manager.stop_all()
        ```
    """

    def __init__(self):
        self.tasks: list[BackgroundTask] = []

    def add(self, task: BackgroundTask) -> None:
        """Add a background task."""
        self.tasks.append(task)

    async def start_all(self) -> None:
        """Start all registered tasks."""
        await asyncio.gather(*[t.start() for t in self.tasks])

    async def stop_all(self, timeout: float = 30.0) -> None:
        """Stop all tasks gracefully."""
        await asyncio.gather(*[t.stop(timeout / len(self.tasks)) for t in self.tasks])
```

---

## Dependency Injection Pattern

FastAPI dependency injection for clean, testable code.

```python
from functools import lru_cache
from typing import Annotated, AsyncGenerator

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config.settings import Settings


# =============================================================================
# Settings
# =============================================================================

@lru_cache
def get_settings() -> Settings:
    """Get application settings (singleton).

    Uses lru_cache for singleton behavior - settings are loaded once
    and reused for all requests.
    """
    return Settings()


# Type alias for cleaner endpoint signatures
SettingsDep = Annotated[Settings, Depends(get_settings)]


# =============================================================================
# Database
# =============================================================================

def get_engine(settings: SettingsDep):
    """Create database engine (singleton via settings cache)."""
    return create_async_engine(settings.postgres.url, pool_size=5, max_overflow=10)


def get_session_factory(engine = Depends(get_engine)) -> async_sessionmaker:
    """Create session factory."""
    return async_sessionmaker(engine, expire_on_commit=False)


async def get_db(
    session_factory: async_sessionmaker = Depends(get_session_factory),
) -> AsyncGenerator[AsyncSession, None]:
    """Get database session for request.

    Provides a session that is automatically closed after the request.
    """
    async with session_factory() as session:
        try:
            yield session
        finally:
            await session.close()


# Type alias
DbSession = Annotated[AsyncSession, Depends(get_db)]


# =============================================================================
# Repositories
# =============================================================================

def get_user_repo(db: DbSession) -> "UserRepository":
    """Get user repository."""
    return SQLAlchemyRepository(db, User)


def get_order_repo(db: DbSession) -> "OrderRepository":
    """Get order repository."""
    return SQLAlchemyRepository(db, Order)


# Type aliases
UserRepoDep = Annotated["UserRepository", Depends(get_user_repo)]
OrderRepoDep = Annotated["OrderRepository", Depends(get_order_repo)]


# =============================================================================
# Services
# =============================================================================

def get_email_notifier(settings: SettingsDep) -> "EmailNotifier":
    """Get email notifier service."""
    return EmailNotifier(settings.smtp)


def get_user_service(
    repo: UserRepoDep,
    notifier: Annotated["EmailNotifier", Depends(get_email_notifier)],
) -> "UserService":
    """Get user service with all dependencies."""
    return UserService(repo, notifier)


def get_order_service(
    order_repo: OrderRepoDep,
    user_repo: UserRepoDep,
) -> "OrderService":
    """Get order service."""
    return OrderService(order_repo, user_repo)


# Type aliases
UserServiceDep = Annotated["UserService", Depends(get_user_service)]
OrderServiceDep = Annotated["OrderService", Depends(get_order_service)]


# =============================================================================
# Usage Example
# =============================================================================

# In your router file:
#
# from fastapi import APIRouter
#
# router = APIRouter(prefix="/users", tags=["users"])
#
# @router.post("/")
# async def create_user(
#     data: CreateUserRequest,
#     service: UserServiceDep,
# ) -> User:
#     """Create a new user."""
#     result = await service.create_user(data)
#     if not result.success:
#         raise HTTPException(400, result.error)
#     return result.data
#
# @router.get("/{user_id}")
# async def get_user(
#     user_id: str,
#     repo: UserRepoDep,
# ) -> User:
#     """Get user by ID."""
#     user = await repo.get(user_id)
#     if not user:
#         raise HTTPException(404, "User not found")
#     return user


# =============================================================================
# Testing
# =============================================================================

# For testing, override dependencies:
#
# from fastapi.testclient import TestClient
#
# def get_mock_user_repo() -> UserRepository:
#     return MockUserRepository()
#
# app.dependency_overrides[get_user_repo] = get_mock_user_repo
#
# with TestClient(app) as client:
#     response = client.post("/users/", json={"email": "test@example.com"})
```

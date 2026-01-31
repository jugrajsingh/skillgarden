# FastAPI Diagnostic Patterns

## Common Errors

| Error | Likely Cause | Check |
|-------|-------------|-------|
| 422 Unprocessable Entity | Pydantic validation failure — missing field, wrong type, or failed validator | Read response body `.detail` array; each entry has `loc`, `msg`, `type` |
| 422 on GET with body | FastAPI ignores GET request bodies by default | Move params to query parameters or change to POST |
| `value is not a valid dict` | Passing raw dict where Pydantic model expected, or JSON string not parsed | Check if endpoint expects `Model` but receives `dict` |
| `TypeError: object X can't be used in 'await' expression` | Calling sync function with await, or async def missing from dependency | Verify function is actually async; check dependency return type |
| `RuntimeError: Event loop is already running` | Blocking call inside async context (sync ORM, `time.sleep`, CPU-bound) | Replace with async equivalent or run in `run_in_executor` |
| Dependency returns None unexpectedly | Yield-based dependency with exception before yield | Add try/except around yield in dependency; check generator flow |
| CORS errors in browser | `CORSMiddleware` not added or added after route registration | Verify middleware order — CORS must be added before routes |
| `Depends()` not injecting | Missing `Depends()` wrapper, or parameter has default value hiding the dependency | Check function signature — `db = Depends(get_db)` not `db = get_db` |
| Slow startup / hanging | Blocking I/O in lifespan or startup event | Move blocking calls to background tasks or use async variants |
| `starlette.routing.NoMatchFound` | Route ordering — more specific routes shadowed by parameterized routes | Place specific routes before `/{param}` catch-all routes |

## Gotchas

- Middleware executes in reverse order of addition — last added runs first on request
- `BackgroundTasks` run after response is sent but share the same event loop — blocking calls stall everything
- `response_model` silently filters fields not in the model — data appears "missing" but is just excluded
- Path parameters are strings by default — `/{id}` gives `str`, use `/{id: int}` for auto-conversion
- `Depends` with `yield` runs cleanup AFTER response — exceptions in cleanup don't reach the client
- `TestClient` runs sync — async dependencies may behave differently than in production
- `HTTPException` inside dependencies is caught by FastAPI, but generic `Exception` is not — returns 500

## Diagnostic Commands

```bash
# Check installed FastAPI and Pydantic versions (v1 vs v2 is a common source of breaks)
pip show fastapi pydantic uvicorn

# Run with debug reload and verbose logging
uvicorn app.main:app --reload --log-level debug

# Test specific endpoint with full response
curl -v -X POST http://localhost:8000/endpoint -H "Content-Type: application/json" -d '{}'

# Check registered routes
python -c "from app.main import app; [print(r.path, r.methods) for r in app.routes]"

# Validate Pydantic model independently
python -c "from app.models import MyModel; MyModel.model_validate({'field': 'value'})"
```

## Known Patterns

- **Pydantic v1 → v2 migration:** `.dict()` → `.model_dump()`, `.parse_obj()` → `.model_validate()`, `validator` → `field_validator`. Mixing versions causes silent failures
- **Circular import at startup:** FastAPI eagerly imports route modules — circular deps between models and routes crash on import. Fix: move shared models to separate module
- **Missing async driver:** Using `sqlalchemy` with async FastAPI but forgot `asyncpg` or `aiosqlite` — falls back to sync, blocks event loop
- **Gunicorn + uvicorn workers:** `gunicorn -k uvicorn.workers.UvicornWorker` — forgetting `-k` flag runs sync gunicorn workers, async code breaks silently
- **Lifespan vs on_event:** `@app.on_event("startup")` is deprecated in favor of lifespan context manager — mixing both causes double initialization

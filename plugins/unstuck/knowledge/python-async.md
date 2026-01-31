# Python Async Diagnostic Patterns

## Common Errors

| Error | Likely Cause | Check |
|-------|-------------|-------|
| `RuntimeError: Event loop is already running` | Calling `asyncio.run()` inside an already-running loop (Jupyter, nested async) | Use `await` directly or `nest_asyncio.apply()` in notebooks |
| `RuntimeError: no current event loop` | Accessing loop from a thread that didn't create one | Use `asyncio.get_event_loop()` or pass loop explicitly; in 3.10+, use `asyncio.Runner` |
| `Task was destroyed but it is pending` | Task created but never awaited or cancelled before loop close | Store task references; cancel and await in shutdown |
| `coroutine 'X' was never awaited` | Missing `await` keyword — called async function without awaiting | Add `await` before the coroutine call |
| `TypeError: object coroutine can't be used in 'await' expression` | Awaiting a non-awaitable or double-awaiting | Check if function is actually async; don't `await await` |
| `asyncio.TimeoutError` with no traceback | `asyncio.wait_for` timed out — cancels the inner task silently | Wrap in try/except; check if timeout is too aggressive |
| `CancelledError` propagating unexpectedly | Task cancelled during `await`; in 3.9+ it inherits from `BaseException` | Catch `CancelledError` explicitly if cleanup needed |
| Deadlock / program hangs | Blocking sync call in async context (`time.sleep`, sync I/O, CPU-bound) | Use `await asyncio.sleep()`, `run_in_executor`, or `asyncio.to_thread` |
| `gather` swallows exceptions silently | Using `return_exceptions=True` without checking results | Iterate results; `isinstance(r, Exception)` to find failures |
| Connection pool exhausted | Too many concurrent connections; not releasing back to pool | Use `async with` for connections; limit concurrency with `Semaphore` |

## Gotchas

- `asyncio.gather` with `return_exceptions=False` (default) cancels remaining tasks on first exception — often not what you want
- `async for` requires `__aiter__`/`__anext__` — regular iterators silently fail or behave unexpectedly
- `asyncio.create_task()` without storing the reference — task can be garbage collected before completion
- Signal handlers (SIGTERM, SIGINT) only work on the main thread — workers need different shutdown patterns
- `asyncio.Lock` is NOT thread-safe — only protects against concurrent coroutines, not threads
- `async with` on database connections — forgetting causes connection leaks under load
- `asyncio.Queue.get()` blocks the coroutine but not the thread — use `get_nowait()` for non-blocking checks
- Python 3.12 changed `TaskGroup` exception handling — `ExceptionGroup` replaces individual exception propagation

## Diagnostic Commands

```bash
# Check Python version (async behavior differs significantly between 3.8-3.12)
python --version

# Enable asyncio debug mode for detailed warnings
PYTHONASYNCIODEBUG=1 python app.py

# Profile event loop blocking
python -X dev -W default app.py

# Check for blocking calls in async code
grep -rn "time\.sleep\|\.connect()\|\.execute(" --include="*.py" | grep -v "await"

# List running tasks (add to code for debugging)
# import asyncio; [print(t.get_name(), t.get_coro()) for t in asyncio.all_tasks()]
```

## Known Patterns

- **Blocking the event loop:** Most common async issue. Sync HTTP clients (`requests`), sync DB drivers (`psycopg2`), `time.sleep()`, CPU-heavy computation — all block the loop. Fix: async libraries (`httpx`, `asyncpg`, `aiosqlite`) or `asyncio.to_thread()`
- **Fire-and-forget tasks:** `asyncio.create_task(coro())` without storing reference — task silently disappears on GC. Fix: store in a set, `tasks.add(t); t.add_done_callback(tasks.discard)`
- **Graceful shutdown:** `KeyboardInterrupt` in async code leaves pending tasks. Fix: signal handler that sets a flag, `await asyncio.gather(*pending, return_exceptions=True)` in shutdown
- **Semaphore for concurrency control:** Unbounded `gather` on 10k items overwhelms resources. Fix: `sem = asyncio.Semaphore(50); async with sem: await work()`
- **Exception in TaskGroup:** Python 3.11+ `TaskGroup` raises `ExceptionGroup` — catch with `except*` syntax or use `exceptiongroup` backport

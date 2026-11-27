## FastAPI (Python)
- Feature folders with `router`, `schemas`, `service`, `repository/models`; routers thin.
- Pydantic schemas separate from ORM models; response models declared (`response_model`) so internals/passwords do not leak.
- Dependencies via `Depends` (DB session, current user); one session per request, closed properly; auth dependency on every protected router.
- `async def` handlers do not call blocking I/O or sync ORM without a threadpool; consistent sync or async stack.
- Version check: recent FastAPI releases require Pydantic v2 (v1 support was dropped in the 0.12x series per the official migration guide); Pydantic v1 code (`class Config`, `@validator`, `.dict()`) on a new FastAPI is a defect or a pinned-old-version smell. `@app.on_event` is deprecated in favor of a `lifespan` context manager (removal version not verified).
- Settings via `pydantic-settings`; `DEBUG`/CORS configured per environment; migrations (Alembic) committed.

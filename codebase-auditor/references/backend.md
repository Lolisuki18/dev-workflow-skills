# Backend Checklist

Check only what applies to the detected framework. Cite `file:line` for every hit.

## Architecture & layering
- Controllers/routes contain only transport concerns (parse, validate, call service, map response); business logic lives in services/domain.
- No data-access code (queries, ORM calls) inside controllers; no HTTP types leaking into domain/service code.
- Clear module boundaries; no circular imports/dependencies; no "god" service/class (> ~500 lines or many unrelated responsibilities).
- Consistent naming and folder conventions; duplicated logic that should be one helper.
- Configuration injected, not read ad hoc from globals/env scattered across code.

## API design & validation
- Every public endpoint validates input (type, length, range, format) server-side with a schema/DTO.
- Consistent response and error format; correct HTTP status codes; no stack traces returned to clients.
- Pagination/limits on list endpoints; no unbounded queries.
- Idempotency for payments/retries where relevant; versioning strategy if public.
- Mass assignment: request bodies not bound directly to entities/models.

## Data access & database
- Parameterized queries / ORM only; flag string-concatenated SQL/NoSQL filters.
- N+1 queries in loops; missing indexes on filtered/joined columns (check migrations/schema).
- Transactions around multi-step writes; correct rollback on error.
- Migrations present and ordered; no destructive migration without guard; schema matches entities.
- Connection handling: pooling, closed resources, no connection per request.
- Sensitive columns (passwords, tokens) stored hashed/encrypted; soft-delete and cascade rules intentional.

## Error handling & reliability
- Central error handler; no empty `catch`/`except` that swallows errors; errors keep context.
- Timeouts and retries on outbound HTTP/DB/queue calls; no blocking calls in async paths.
- Race conditions on read-modify-write (counters, balances, stock, coupons); unique constraints backing "check then insert".
- Money/currency calculations use integer minor units or decimal types (no binary float rounding drift); reject `NaN`/negative/oversized amounts.
- Background jobs idempotent; graceful shutdown.

## Concurrency & performance
- Shared mutable state in singletons/modules without synchronization.
- Heavy work on the request thread; missing caching where obviously repeated.
- Large payloads loaded fully into memory (file uploads, exports).

## Testing & quality
- Tests exist for core business logic and auth; failing/skipped tests; tests that assert nothing.
- Lint/type-check configured; dead code, unused dependencies, commented-out blocks.
- Debug leftovers: `print`, `console.log`, `System.out.println`, `var_dump`, TODO/FIXME on critical paths.

## Stack-specific hints (only if detected)
- **Node/Express/Nest:** unhandled promise rejections, missing `await`, middleware order (auth before routes), body size limits.
- **Python/Django/FastAPI/Flask:** `DEBUG=True` in prod config, `ALLOWED_HOSTS`, raw queries, blocking calls in async handlers, mutable default args.
- **Java/Spring:** `@Transactional` on private/self-invoked methods, entities exposed as API models, lazy-loading outside session, field injection overuse.
- **.NET:** missing `async` all the way, `DbContext` lifetime, model validation attributes unused, exceptions as control flow.
- **Go:** goroutine leaks (no exit path, channel never read), missing `context` propagation/cancellation, ignored or unwrapped errors (`%w`), `defer` inside loops (runs at function end), data races on shared maps/state (`go test -race` if runnable), `net/http` server without timeouts and `http.DefaultClient` without a timeout, response bodies not closed, SQL built with `fmt.Sprintf` instead of `database/sql` placeholders, `rows.Close()`/`rows.Err()` unchecked, loop variable captured by a goroutine (depends on the `go` version in `go.mod`).
- **Rust:** `unsafe` without a safety justification, `unwrap`/`expect`/indexing on user input, panics reachable from request handlers, `.clone()` used to dodge ownership, lifetime-heavy APIs that could own their data, integer overflow (wraps in release builds unless overflow checks are enabled; use `checked_*`/`saturating_*` on untrusted arithmetic), blocking calls or `std::sync::Mutex` guards held across `.await`, `cargo clippy` warnings suppressed wholesale, `cargo audit` not in CI.
- **PHP/Laravel, Rails:** apply the generic items above; verify framework-specific claims in the code before reporting.

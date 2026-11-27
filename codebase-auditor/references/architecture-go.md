## Go (services / CLIs)
- Packages by feature under `internal/`; `main` only wires config and dependencies; no package-level mutable globals for DB/clients; no import cycles; no `util`/`common` dumping ground.
- Interfaces are small and defined by the consumer; flag an interface only if it is clearly pure ceremony (one trivial implementation, used nowhere else).
- Handlers decode, validate, call a service, encode; no SQL in handlers. `context.Context` is the first parameter and flows from the request to DB/HTTP calls.
- Errors are returned and wrapped with `%w`; no ignored `err` (`_ =`) on I/O or DB calls; `panic` only for programmer errors, with `recover` at the server boundary if used.
- `http.Server` has read/write/idle timeouts (or `ReadHeaderTimeout`); outbound `http.Client` has a timeout; graceful shutdown on signal.

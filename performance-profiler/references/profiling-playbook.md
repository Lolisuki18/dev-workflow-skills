# Profiling playbook

Pick tools already in the repo first. Check each tool's current docs for exact flags before using it; do not guess options.

## Measure first

- Repeat runs (at least 5), drop the first, report median and spread.
- Same data, same machine, same load; note CPU model, runtime version, cache state (cold or warm).
- Prefer measuring the real code path (a benchmark that calls the real function or endpoint) over a micro-benchmark of an isolated piece.

## Tools by area (examples, not a requirement)

| Area | Typical tools |
|---|---|
| Node.js | built-in `--cpu-prof` / `--inspect`, `console.time` for coarse checks, `autocannon` for HTTP |
| Python | `cProfile` + `pstats`, `timeit`, `tracemalloc` for memory, `py-spy` for a running process |
| Java / Kotlin | JFR (Java Flight Recorder), VisualVM, JMH for micro-benchmarks |
| .NET | `dotnet-trace`, `dotnet-counters`, BenchmarkDotNet |
| Go | `pprof`, `go test -bench` |
| SQL | `EXPLAIN` / `EXPLAIN ANALYZE`, slow query log, check the plan before and after adding an index |
| Browser / front end | DevTools Performance and Network panels, Lighthouse, bundle analyzer |
| Build and CI | timing per step, cache hit rates, `time` on each command |

## Common causes (check against evidence, do not assume)

| Symptom | Look for |
|---|---|
| Many similar queries per request | N+1: query inside a loop, lazy loading in a serializer |
| One slow query | missing or unused index, `SELECT *`, large offset pagination, function on an indexed column |
| High CPU in app code | work repeated inside loops, regex compiled each call, repeated JSON parsing, sorting large lists repeatedly |
| Growing memory | unbounded caches or lists, listeners never removed, loading a whole file or table |
| Slow only under concurrency | lock contention, connection pool too small, synchronous I/O in a hot path |
| Slow first load in the browser | large bundles, render-blocking requests, unoptimized images, no compression or caching headers |
| Slow build | no dependency cache, tests run serially that could be split, rebuilding unchanged parts |

## Reporting rules

- A gain smaller than the run-to-run spread is not a gain.
- State what was not measured (other inputs, production hardware, cache effects).
- Keep the benchmark script in the repo only if the user wants it; otherwise leave it in the report.

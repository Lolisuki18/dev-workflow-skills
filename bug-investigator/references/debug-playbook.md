# Debug Playbook

## Reading logs and stack traces
- Find the FIRST error in time order; later errors are often consequences.
- In a stack trace, the top frame is where it failed, but the cause is usually the first frame in YOUR code. Read the "Caused by" chain to the bottom.
- Use timestamps and request/correlation ids to follow one request across services.
- Compare a failing request with a successful one: diff inputs, headers, user, data, timing.
- Mask secrets and personal data when quoting logs.

## Narrowing techniques
- **Minimal reproduction:** remove inputs/steps until the bug disappears, then add back the last one.
- **Bisect:** `git bisect` between a known good and bad commit; or bisect config/data/dependency versions.
- **Diff the environment:** versions, env vars, OS, locale/timezone, database content, feature flags.
- **Binary search in code:** assert/log the value midway through the flow to see which half is wrong.
- **Change one thing at a time**; write down each experiment and its result.

## Common root causes by symptom

| Symptom | Check first |
|---------|-------------|
| `null`/`undefined`/`NoneType` errors | Missing data or async not awaited; optional field assumed present; wrong default |
| Works locally, fails in prod/CI | Env vars, config, versions, case-sensitive paths, timezone, memory/timeouts, build vs dev mode |
| Intermittent failure | Race conditions, shared mutable state, caching/stale data, test order dependence, time-based logic, retries |
| Wrong result, no error | Off-by-one, integer/float or rounding, timezone/DST, string vs number comparison, mutation of shared object, wrong join/filter |
| Slow / timeout | N+1 queries, missing index, unbounded list, blocking call in async path, repeated renders/requests |
| 401/403/404 on valid action | Token expiry/clock skew, wrong tenant/user, route order, CORS/proxy path rewriting, trailing slash |
| 500 after deploy | Missing migration, new env var not set, dependency version drift, changed contract between services |
| UI shows stale/blank data | Missing loading/empty/error state, cache key wrong, effect dependencies, state mutated in place |
| Data corruption / duplicates | Missing transaction or unique constraint, non-idempotent retry, double submit |
| Memory growth / crash | Unclosed resources/listeners/subscriptions, unbounded caches, large payloads loaded whole |
| Test fails only sometimes | Time/random not controlled, shared state between tests, async not awaited, external services |

## Evidence checklist before declaring root cause
- [ ] I can trigger the bug on demand (or I stated why not).
- [ ] The cause explains every observed symptom and the timing.
- [ ] I tried to falsify it (a case where, if my theory is right, the bug must NOT happen, and verified it).
- [ ] I know why it was not caught earlier.
- [ ] I searched for the same pattern elsewhere.

## Fix quality checklist
- [ ] Regression test fails before, passes after, for the right reason.
- [ ] Minimal diff; no unrelated changes.
- [ ] Error handling does not just swallow the symptom.
- [ ] Debug output removed; lint/type-check clean.

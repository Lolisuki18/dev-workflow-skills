# Security & Operations Checklist

Stack-agnostic. Cite `file:line`. Calibrate severity to the project's scale (MVP vs Production).

## Secrets & configuration
- Hard-coded passwords, API keys, tokens, private keys, connection strings in code, tests, Dockerfiles, CI files, notebooks. Check git-tracked `.env*`, `*.pem`, `*.key`, `credentials*.json`.
- `.gitignore` covers `.env`, build output, local DBs, IDE files; `.env.example` exists with placeholders only.
- Different config per environment; debug flags (`DEBUG=True`, verbose errors, dev CORS `*`) off in production config.
- If a live-looking secret is found: report it as Critical, name only the variable/type and `file:line` (never print any secret characters, per `CONVENTIONS.md`), and recommend rotation.

## Authentication & authorization
- Passwords hashed with a modern algorithm (bcrypt/argon2/scrypt); never plain text or fast hashes (MD5/SHA1).
- Session/JWT: strong secret from env, expiry set, signature algorithm pinned, refresh/revocation approach, secure/httpOnly/sameSite cookies.
- Authorization enforced server-side on EVERY protected route/resource; check object-level access (user A cannot read user B's record by changing an id).
- Rate limiting / lockout on login, signup, password reset, OTP.
- Admin/internal endpoints not publicly reachable; default credentials removed.

## Input, injection & output
- SQL/NoSQL/command/template injection: user input concatenated into queries, shell commands, file paths.
- Path traversal and unrestricted file upload (type, size, storage location, served as executable).
- SSRF on user-supplied URLs; XML/YAML deserialization of untrusted data; `eval`/`exec` on input.
- Output encoding (XSS); CSRF protection for cookie-based auth; CORS allow-list rather than `*` with credentials.
- Security headers where relevant (CSP, HSTS, X-Content-Type-Options).

## Data protection & privacy
- Sensitive data (PII, tokens, passwords) not written to logs, URLs, error messages or analytics.
- TLS for all external traffic; encrypted at rest where required; backups and retention considered.
- Minimal data collection; deletion/export path if the app handles personal data.

## Dependencies & supply chain
- Lockfile committed; unpinned or very outdated critical dependencies; unused dependencies.
- Run the ecosystem's audit command if available (e.g. `npm audit`, `pip-audit`, `mvn dependency-check`, `dotnet list package --vulnerable`, `flutter pub outdated`) and cite real output; if not runnable, state that.
- Suspicious/typosquatted packages, install scripts, packages fetched from unknown registries or git URLs.

## Logging, monitoring & errors
- Structured logs with levels; no leftover debug output; request correlation ids where multiple services exist.
- Errors captured (Sentry/log aggregation) in production-scale projects; health-check endpoint.
- Alerts or at least visibility for failures in background jobs.

## Build, deploy & CI/CD
- Dockerfile: non-root user, pinned base image, no secrets baked into layers, `.dockerignore`, multi-stage build for production.
- CI runs lint, type-check, tests; pipeline secrets stored in the CI secret store; no deploy from unreviewed branches.
- Reproducible build and documented run steps (README); database migration step in deploy process; rollback plan for production-scale projects.
- Infrastructure files (compose, k8s, terraform): exposed ports and databases open to the internet, wildcard IAM permissions, default passwords.

## Repository hygiene
- Committed build artifacts, `node_modules`, large binaries, local DB files, IDE configs with personal paths.
- README accuracy; license present if public; no leftover TODO/FIXME on security-critical paths.
- Git history: secrets that were committed and later removed still live in history (report as a rotation item).

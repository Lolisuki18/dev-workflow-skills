# Security checklist (by area)

Use only the parts that match the stack. Each line is a question to answer from code.

## Authentication
- Passwords hashed with a slow, salted algorithm (bcrypt, scrypt, argon2). Not MD5/SHA-1/plain.
- Login, reset and OTP endpoints are rate limited; error messages do not reveal whether an account exists.
- Tokens: signature verified, `alg` pinned, expiry set, refresh tokens rotated or revocable; secrets not hardcoded.
- Cookies: `HttpOnly`, `Secure`, `SameSite` set; session id regenerated after login.

## Authorization
- Every state-changing and data-returning route checks permission on the server, not only in the UI.
- Object-level checks: the id in the URL or body is verified to belong to the caller (IDOR / BOLA).
- Admin and internal routes are not reachable by a normal user by guessing the path.
- Mass assignment: request bodies are not bound directly to models with fields like `role` or `isAdmin`.

## Injection and unsafe sinks
- SQL: parameterized queries or ORM binding; no string concatenation with user input. Check raw-query helpers and `ORDER BY` / `LIMIT` built from input.
- Shell: no `exec` / `system` with user input; arguments passed as arrays.
- HTML: output encoding by default; search for `dangerouslySetInnerHTML`, `v-html`, `innerHTML`, `|safe`, `Html.Raw`.
- SSRF: user-supplied URLs fetched by the server are restricted (allow-list, no internal ranges, no redirects to them).
- Files: upload type and size checks, random server-side names, storage outside the web root, path joins checked against `..`.
- Deserialization and XML parsers: no untrusted native deserialization, external entities disabled.
- Redirects: target validated against an allow-list.

## Secrets and configuration
- Search the repo and git history for keys, tokens, private keys and connection strings (`git log -p -S` on suspicious names). Report type and location only.
- `.env` and credential files are git-ignored; example files hold placeholders.
- Debug flags, stack traces and admin consoles are off in production configuration.
- CORS is not `*` together with credentials; CSRF protection exists for cookie-based sessions.

## Data protection
- Responses return only needed fields (no password hash, internal ids, other users' PII).
- Logs do not contain passwords, tokens, card numbers or full request bodies of sensitive endpoints.
- TLS enforced; sensitive columns encrypted where the data class requires it.

## Dependencies and supply chain
- Lockfile committed; versions pinned.
- Name each vulnerable package with version and advisory id only after checking the advisory source; do not guess CVE numbers.
- Install scripts and unusual packages (typosquats, abandoned) flagged.

## Business logic
- Price, quantity, discount and balance computed on the server; negative and huge values rejected.
- Workflows cannot skip steps (pay before ship, verify before login).
- Race conditions on balance, stock and coupon use have locking or unique constraints.

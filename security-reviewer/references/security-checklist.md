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

## CLI / local tool
- Untrusted file paths (arguments, config, data files) are not trusted to stay inside an intended directory.
- Symlinks: the tool does not follow a link into a file the user did not name.
- Temp files are created with safe names and permissions (not predictable, not world-writable).
- Writes are atomic (write to a temp file, then rename); a crash does not leave a partial or empty data file.
- Data printed to the terminal (names, notes, file contents) cannot inject escape sequences that rewrite the screen.
- Concurrent runs cannot cause a lost update (read-modify-write without a lock).
- Secrets are not passed in command-line arguments or environment variables that other users or logs can see.
- Integrity-only issues (a user damaging their own local file) are Low; raise severity only when another user or a privilege boundary is involved.

## Business logic
- Price, quantity, discount and balance computed on the server; negative and huge values rejected.
- Workflows cannot skip steps (pay before ship, verify before login).
- Race conditions on balance, stock and coupon use have locking or unique constraints.

## BaaS, Mobile & Framework Pitfalls
- Supabase/Firebase: Row Level Security (RLS) enabled with explicit policies on every exposed table; `service_role` / admin credentials never shipped in client bundles.
- ASP.NET Core Minimal APIs: DataAnnotations (`[Range]`, `[Required]`) are ignored unless `builder.Services.AddValidation()` (.NET 10+) or an endpoint filter is registered.
- NestJS: `ValidationPipe` needs `forbidNonWhitelisted: true` (alongside `whitelist: true`) to reject unknown fields, and `@UseGuards` / `APP_GUARD` on protected routes.
- Go: SQL built with `fmt.Sprintf` instead of `database/sql` placeholders; `http.Server` without read/header timeouts and `http.Client` without timeout; request bodies not capped (`http.MaxBytesReader`); `math/rand` used for tokens or IDs (use `crypto/rand`); `InsecureSkipVerify: true`; `exec.Command("sh", "-c", input)`; user input in `filepath.Join` without a check against `..`; `text/template` used for HTML (`html/template` escapes). Run `govulncheck ./...` if available.
- Rust: `unsafe` blocks without a justification; `unwrap`/`expect`/indexing on user input (panic = denial of service); panics reachable from handlers; arithmetic on untrusted numbers (release builds wrap on overflow unless overflow checks are enabled; use `checked_*`); SQL via `format!` instead of bound parameters; `Command::new("sh").arg("-c")` with input. Run `cargo audit` if available.
- Android: components with intent filters and no deliberate `android:exported`; exported content providers/receivers/services without permission checks; implicit intents carrying sensitive data; mutable `PendingIntent`s; `android:allowBackup` and `usesCleartextTraffic` left on; WebView with `setJavaScriptEnabled(true)` or `addJavascriptInterface` on untrusted content; API keys/secrets in `BuildConfig`, `strings.xml` or source (an APK can be unpacked); tokens in plain `SharedPreferences` instead of Android Keystore-backed storage; sensitive data in `Log`; unvalidated deep links.
- iOS: App Transport Security disabled or broadly excepted (`NSAllowsArbitraryLoads`); tokens, passwords or keys in `UserDefaults`, plist files or source instead of Keychain (check the `kSecAttrAccessible` level); URL schemes / universal links used without validating parameters; `WKWebView` loading untrusted content with a JavaScript bridge; sensitive data in `print`/`NSLog`/analytics; secrets embedded in the app bundle.

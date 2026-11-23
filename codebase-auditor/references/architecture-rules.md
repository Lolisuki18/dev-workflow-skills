# Architecture Rules (audit against the project's own style)

**Verification status (checked 2026-11-23 via web search of official/primary pages):**
- Verified: Next.js 16 (`proxy.ts` replaces `middleware.ts`; official Data Access Layer guidance), Spring Boot 4 / Framework 7 (Jackson 3 default, JSpecify null-safety), MediatR v13+ licensing, FastAPI + Pydantic v2 status.
- Second pass (same date): NestJS `ValidationPipe` options, Flutter `BuildContext`/`mounted` lint, Supabase RLS and key handling, Spring `open-in-view`, EF Core tracking/lifetime/pooling were checked against search results (official docs where they were returned, otherwise reputable secondary sources).
- Weakly verified: the Firebase "test mode expires after ~30 days" behavior (only community sources found, no official wording), Spring Boot 4's `open-in-view` default, exact FastAPI `on_event` removal version. Marked in the text.
- NOT re-verified: Hibernate-specific behavior beyond the above, EF Core migrations, NestJS guard/module details, Firestore rule syntax. Treat those as general practice.
- Always detect the project's actual framework version first (lockfile/manifest, cite `file:line`) and judge against THAT version's docs; a rule below that does not apply to the installed version is not a finding.

How to use:
1. Determine the architecture the project DECLARES (README, `plan/` "Impact on architecture", docs) or, failing that, the one it clearly uses (folder structure). Cite the evidence.
2. Judge the code against that style. Do NOT demand Clean Architecture from a feature-based MVP, or the reverse. Mixed/unclear structure is itself a Medium finding.
3. Apply the matching stack section below. Skip sections for stacks not present. Cite `file:line` for every violation.

## Style rules

### Feature-based
- Each feature folder is cohesive (UI/handlers, logic, data access, types together).
- Features do not reach into each other's internals; cross-feature use goes through a small public surface (index/exports, service interface, events). Flag deep imports like `features/a/internal/...` from feature b.
- Shared code lives in an explicit `shared/`/`common/` folder and contains no feature-specific logic; flag a "utils" dump growing business rules.
- No circular imports between features.

### Clean / Hexagonal
- Dependency rule: Domain imports nothing from Application, Infrastructure, web or framework packages. Application imports Domain only. Flag any inward-pointing violation (e.g. entity annotated with web/serialization concerns, domain importing ORM or HTTP types).
- Use cases/handlers hold orchestration; entities hold business invariants; controllers hold only transport concerns.
- Infrastructure implements interfaces (ports) declared in Application/Domain; no concrete DB client used directly in use cases.
- Mapping between layers is explicit; persistence entities are not returned from the API.
- Flag needless ceremony only if it is clearly pure pass-through (interfaces with one trivial implementation on a tiny CRUD app) — Low.

### Hybrid
- Feature-based top level, layering inside features; check both sets of rules at their own level.

## Next.js (App Router) + TypeScript + Prisma/Drizzle
- `app/` holds routing, layouts and thin pages; business logic and queries live in `features/`/`lib/`, not inside page components.
- Server vs client: `'use client'` only on leaf components that need state/effects/browser APIs; flag whole pages/layouts marked client without need.
- DB/ORM calls only in server code (Server Components, Server Actions, route handlers, a data-access layer). Flag Prisma/Drizzle imports reachable from client components; prefer a `server-only` boundary.
- Every Server Action and route handler: validates input with a schema (Zod), checks authentication AND authorization/ownership, returns a typed result; never trusts client-provided user ids.
- Official guidance (Next.js data-security guide): prefer a server-only Data Access Layer that performs the authorization check and returns minimal DTOs, so components/actions never receive raw DB rows. Flag direct ORM rows passed to client components.
- Server Actions are public POST endpoints: each needs its own authN/authZ check even if the page is protected. Proxy/middleware (Next.js 16: `proxy.ts`, formerly `middleware.ts`) is for optimistic redirects, not the only authorization layer; flag auth enforced only there or only in a layout.
- Next.js ≥16: `middleware.ts` still works but is deprecated in favor of `proxy.ts` (Low, upgrade note). The experimental taint API is defense in depth only, not a substitute for DTOs.
- Secrets never in `NEXT_PUBLIC_*`; env access centralized and validated.
- `loading.tsx`/`error.tsx`/`not-found.tsx` present for data-driven segments; cache/revalidation (`revalidatePath/Tag`) after mutations is deliberate.
- Prisma/Drizzle: client singleton (no new client per request in dev hot reload), migrations committed, multi-write operations in a transaction.

## Spring Boot (Java)
- Controller → Service → Repository; controllers contain no business logic or repository calls; services do not touch `HttpServletRequest`.
- DTOs (records) separate from JPA entities; entities never serialized to clients; mapping in a mapper/assembler.
- `@Transactional` on service methods (public, called from another bean — self-invocation does not apply it); read-only for queries; no transactions in controllers.
- Constructor injection (flag field `@Autowired`); configuration via `@ConfigurationProperties`, not scattered `@Value` strings.
- Input validation with `@Valid` + Bean Validation on request DTOs; central `@RestControllerAdvice` for errors with a consistent error body.
- JPA: LAZY relations accessed inside a transaction, N+1 (use fetch joins/entity graphs), pagination on lists, `equals/hashCode` sane on entities.
- Open Session in View: `spring.jpa.open-in-view` is enabled when unset (Spring logs a startup warning). It keeps the persistence context open for the whole request, hiding N+1 queries and holding DB connections longer. If the property is unset or `true` on a non-trivial API, report Medium and recommend setting it explicitly (usually `false`, then fixing lazy loading with fetch joins, entity graphs or DTO projections). Whether the default changes in Boot 4 was still being discussed in the project's issue tracker; check the version's reference docs.
- Security: method/route authorization rules present, ownership checks on resource ids, no secrets in `application.yml` committed.
- Version check: Spring Boot 4 / Framework 7 make Jackson 3 the default JSON library (Jackson 2 deprecated) and adopt JSpecify null-safety annotations; Boot 3.x apps are not wrong, but note end-of-support dates (3.5 free support ends June 2026 per reported Spring timelines; verify on spring.io). After a 3→4 upgrade, serialization (dates, nulls, BigDecimal) and Spring Security 7 defaults need re-testing.
- Clean/Hexagonal layout: `domain` has no Spring/JPA annotations (or a documented exception), adapters in/out packages, use-case classes per action.

## ASP.NET Core (.NET)
- Projects/folders Domain, Application, Infrastructure, Api (or Vertical Slice features); Api references Application; Domain references nothing. Flag `.csproj` references that break the rule.
- Controllers/Minimal API endpoints are thin: bind, validate, send to a handler/service, map result. No `DbContext` in controllers.
- `DbContext` and EF Core live in Infrastructure; async all the way (`async/await`, no `.Result`/`.Wait()`), `CancellationToken` passed through; `AsNoTracking` for read-only queries (no change tracking overhead; the result ignores local unsaved changes); no N+1 in loops. `DbContext` registered scoped (one per request), never singleton (not thread-safe). `AddDbContextPool` is only safe when the context class keeps no per-request state in its own fields (pooling resets EF's internal state, not your fields), so flag pooled contexts that inject tenant/current-user state.
- DTOs/contracts separate from entities; validation (DataAnnotations or FluentValidation) on requests; global exception handling (`ProblemDetails`).
- DI lifetimes correct (no scoped service captured by a singleton); options pattern for configuration; secrets via user-secrets/env, not `appsettings.json` committed.
- If MediatR/CQRS is used: commands and queries separated, handlers small, cross-cutting concerns in pipeline behaviors. Do not flag its absence on small apps.
- MediatR licensing: versions from v13 are dual-licensed (RPL-1.5 or commercial; the commercial Community edition is free below a revenue threshold per the author's announcement, check the current terms). Report as a Medium "license review" note for commercial projects using v13+ (cite the `.csproj` `PackageReference` line); v12 and earlier stay on the old license. Same note for AutoMapper v15+. Never claim it is a violation; recommend checking terms or alternatives (plain handlers/services, other mediator libraries).

## NestJS (TypeScript)
- One module per feature (controller, service, dto, entity/schema); modules export only what others need; no circular module imports (`forwardRef` smell).
- Controllers thin; logic in providers/services; repositories or ORM calls not in controllers.
- Global `ValidationPipe` configured deliberately: `whitelist: true` only strips undecorated properties silently; add `forbidNonWhitelisted: true` to reject requests with unknown fields; `transform: true` is needed for payloads to become DTO instances. Whitelisting only affects properties that carry at least one class-validator decorator, so a DTO field with no decorator is dropped (or flagged) — check every body/query/param DTO field is decorated.
- Auth via guards on every protected route; ownership checks in the service; no business authorization only in the frontend.
- Exceptions mapped through filters/`HttpException`; config via `ConfigModule` validated at boot; no `process.env` scattered.

## FastAPI (Python)
- Feature folders with `router`, `schemas`, `service`, `repository/models`; routers thin.
- Pydantic schemas separate from ORM models; response models declared (`response_model`) so internals/passwords do not leak.
- Dependencies via `Depends` (DB session, current user); one session per request, closed properly; auth dependency on every protected router.
- `async def` handlers do not call blocking I/O or sync ORM without a threadpool; consistent sync or async stack.
- Version check: recent FastAPI releases require Pydantic v2 (v1 support was dropped in the 0.12x series per the official migration guide); Pydantic v1 code (`class Config`, `@validator`, `.dict()`) on a new FastAPI is a defect or a pinned-old-version smell. `@app.on_event` is deprecated in favor of a `lifespan` context manager (removal version not verified).
- Settings via `pydantic-settings`; `DEBUG`/CORS configured per environment; migrations (Alembic) committed.

## Flutter (Dart) + Firebase/Supabase
- Feature-first folders; inside each: `data` (repositories, data sources, DTOs), `domain` (entities, use cases — optional on small apps), `presentation` (screens, widgets, state).
- Widgets contain no direct Firestore/Supabase/HTTP calls; they talk to a controller/notifier/bloc that uses a repository.
- One state-management approach used consistently (whichever the project already uses); no business logic in `build()`.
- `dispose()` for controllers/streams/subscriptions; no `BuildContext` use after an `await` without the right `mounted` check: inside a `State`, check `mounted`; for a context passed as a parameter or held in a local, check that context's own `context.mounted` (checking the State's `mounted` while using another context is the classic mistake). The `use_build_context_synchronously` lint covers most cases but is documented as missing uses inside `then()`/`catchError()`/`whenComplete()` callbacks, so read those by hand. `const` constructors where possible.
- Supabase: Row Level Security enabled on every table exposed through the API, with explicit policies (with RLS on and no policies, the publishable/anon key sees nothing; with RLS off, anyone holding the anon key can read the table). The secret / legacy `service_role` key bypasses RLS and must exist only on a server, never in the app bundle, `.env` shipped to the client, or the repo (Critical).
- Firebase: Firestore/Storage rules like `allow read, write: if true` (including "test mode" rules, which community sources say expire after a preset window — confirm the current behavior in the Firebase console) leave the database open to the internet: Critical on production-scale apps, High on a demo holding real user data. Rules should be tested (emulator/Rules Playground) and per-user access scoped by `request.auth.uid`.
- No admin/service credentials in the app bundle; per-user data access scoped by `uid`.
- Loading, empty and error states handled for every async screen.

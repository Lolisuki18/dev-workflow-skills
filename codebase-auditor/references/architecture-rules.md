# Architecture Rules (audit against the project's own style)

Last verified: 2026-11-23
Next review: 2027-05-23
Review process: `docs/maintenance.md` in the repo (re-check each framework against its official docs, update the dates).

**Verification status (checked 2026-11-23 via web search of official/primary pages):**
- Verified: Next.js 16 (`proxy.ts` replaces `middleware.ts`; official Data Access Layer guidance), Spring Boot 4 / Framework 7 (Jackson 3 default, JSpecify null-safety), MediatR v13+ licensing, FastAPI + Pydantic v2 status.
- Second pass (same date): NestJS `ValidationPipe` options, Flutter `BuildContext`/`mounted` lint, Supabase RLS and key handling, Spring `open-in-view`, EF Core tracking/lifetime/pooling were checked against search results (official docs where they were returned, otherwise reputable secondary sources).
- Weakly verified: the Firebase "test mode expires after ~30 days" behavior (only community sources found, no official wording), Spring Boot 4's `open-in-view` default, exact FastAPI `on_event` removal version. Marked in the text.
- NOT re-verified: Hibernate-specific behavior beyond the above, EF Core migrations, NestJS guard/module details, Firestore rule syntax. Treat those as general practice.
- Go, Rust, Android native and iOS native sections (`architecture-go.md`, `architecture-rust.md`, `architecture-android.md`, `architecture-ios.md`) were added from general practice and not checked against current docs; check the project's language/toolchain version before reporting a finding.
- Always detect the project's actual framework version first (lockfile/manifest, cite `file:line`) and judge against THAT version's docs; a rule below that does not apply to the installed version is not a finding.

How to use:
1. Determine the architecture the project DECLARES (README, `plan/` "Impact on architecture", docs) or, failing that, the one it clearly uses (folder structure). Cite the evidence.
2. Judge the code against that style. Do NOT demand Clean Architecture from a feature-based MVP, or the reverse. Mixed/unclear structure is itself a Medium finding.
3. Apply the matching stack section (one `architecture-<stack>.md` file per stack, listed in SKILL.md Step 2). Skip stacks not present. If no listed stack matches (for example a plain stdlib CLI), say "no stack-specific rules apply" and do not force-fit one. Cite `file:line` for every violation.

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

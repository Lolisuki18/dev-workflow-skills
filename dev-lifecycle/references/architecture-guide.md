# Architecture Guide (for Phase 1 — let the user choose)

Use when the stack is known or proposed. Do three things: (1) explain the two styles in plain words, (2) recommend one for THEIR stack with the reason, (3) let them pick. Never impose; record the choice in the Spec Summary and the plan.

## Project level (ask with the stack, record it)

The level sets how much rigor the whole workflow applies. Ask it in the greenfield batch (fold it into the MVP or stack question) with a recommended default; infer it for brownfield from evidence (tests, CI, deploy config, users) and state the inference. Record `Level: <level>` in the Spec Summary and the plan header. The user may change it later.

| Level | Typical project | Default architecture | Test depth | QA / audit strictness | Plan granularity |
|-------|-----------------|----------------------|------------|-----------------------|------------------|
| `fresh` | Coursework, first project, demo | Feature-based, simple layers | Happy path + the key negative cases | Basic: no secrets, no obvious crashes | Small tasks (≤ ~4 h each) |
| `junior` | Thesis, portfolio, side project | Feature-based with layered inside | Unit tests + integration for main flows, boundaries | Standard: validation, auth, error handling | Tasks ≤ ~1 day |
| `mid` | Production app, moderate complexity | Hybrid or Clean | Full pyramid; auth/ownership, rollback, concurrency cases | Strict: security checklist, logging, CI | Feature-level |
| `senior` | Production, high complexity or team-scale | Clean/DDD-style boundaries | As `mid` plus coverage target and critical-path regression suite | Enterprise: threat review, observability, rollback plan | Epic → feature split |

Numbers are suggestions, not gates: do not invent coverage thresholds the user did not choose. Higher level means more checks, not more code: never add layers or tests the level does not call for.

## The two styles in plain words

**Feature-based (tổ chức theo tính năng)**
Group code by what the app does, not by technical type. Each feature (auth, lessons, payments...) has its own folder holding its UI, logic, data access and types. To change "lessons" you open one folder.
- Pros: fast to build and navigate; easy to delete/move a feature; low ceremony; fits small teams.
- Cons: without discipline, features import each other and become tangled; business rules can leak into UI/controllers.

**Clean Architecture (kiến trúc sạch / theo tầng hướng vào trong)**
Split code into layers by responsibility: Domain (pure business rules) → Application (use cases) → Infrastructure/Presentation (DB, web, UI, frameworks). Dependencies point inward only: the domain knows nothing about the framework or database. Hexagonal/"Ports & Adapters" is the same idea.
- Pros: business logic testable without DB/web; swap framework or database easily; scales to complex rules and bigger teams.
- Cons: more files, interfaces and mapping code; slow start; overkill for CRUD-style apps.

**Hybrid (very common in practice):** feature-based folders at the top, a light Clean layering (domain/application/infrastructure, or controller/service/repository) inside each feature.

## Rule of thumb

| Situation | Pick |
|-----------|------|
| MVP, coursework, startup validating an idea, mostly CRUD | Feature-based |
| Complex business rules, long-lived product, several teams/modules, strict testability | Clean (or Hybrid) |
| Not sure | Hybrid: feature-based now, add layers inside a feature only when its logic grows |

## Recommendation per stack (say why, then ask)

| # | Stack | Recommend | Why it fits | Choose the other when |
|---|-------|-----------|-------------|-----------------------|
| 1 | Next.js App Router + TS + PostgreSQL (Prisma/Drizzle) | **Feature-based** (`features/<name>` with `app/` kept thin) | App Router already organizes by route/segment; Server Components and Server Actions colocate UI + server logic; one codebase, few layers needed | Heavy domain logic (billing, workflows) → Hybrid: add `domain/` + `application/` inside those features |
| 2 | React/Next.js + Spring Boot + PostgreSQL/MySQL | **Clean/Hexagonal** (or package-by-feature with Controller→Service→Repository for small apps) | Enterprise Java projects live long and have rich rules; Spring DI, DTO/Entity separation and `@Transactional` map naturally onto layers; common in Vietnamese enterprise hiring | Small/CRUD service → package-by-feature layered is enough |
| 3 | React/Next.js + ASP.NET Core + SQL Server/PostgreSQL | **Clean Architecture** (Domain/Application/Infrastructure/Api projects), optionally Vertical Slice | The .NET community standard; separate projects enforce the dependency rule at compile time; EF Core stays in Infrastructure | Small API → Vertical Slice (feature-based) with Minimal APIs is lighter |
| 4 | React/Vue + NestJS or FastAPI + PostgreSQL | **Feature-based** (NestJS modules / FastAPI feature routers) | NestJS modules and FastAPI routers are already per-feature; fast iteration; Pydantic/DTO validation at the edges is enough structure | Complex domain → Hybrid with `domain/` and `use-cases/` inside the feature |
| 5 | Flutter + Firebase/Supabase | **Feature-first with data/domain/presentation inside** (Hybrid) | Flutter apps grow by screens/features; splitting each feature into UI, state and data keeps widgets free of backend calls and makes testing easy | Tiny app → plain feature folders without a domain layer |
| 6 | Vanilla JS browser app (ES modules, no build, no framework) | **Feature-based, small layers**: pure logic modules, a storage adapter, a DOM layer | No build step means few files and no framework conventions; keeping logic free of the DOM makes it testable with `node:test` | Several unrelated screens → one folder per feature with the same three parts inside |
| 7 | Plain stdlib script / CLI (Python or Node, no packages) | **Flat modules**: pure logic, I/O (files, args) at the edge, a thin `main` | Small surface; pure functions are testable with `unittest` / `node:test` without mocks | Grows past ~5 modules → feature folders |
| 8 | Go service or CLI (`net/http` or a router, `database/sql` / sqlc / pgx) | **Feature-based packages** under `internal/<feature>`, thin `cmd/<app>/main.go` | The package is Go's unit of structure; `internal/` blocks outside imports; deep layering fights the language | Rich domain rules → Hybrid: a `domain` package with no HTTP/SQL imports per feature |
| 9 | Rust service (axum/actix-web + sqlx/diesel), CLI (clap) or library crate | **Feature-based modules** in one crate; Cargo workspace crates when it grows; libraries: small public API re-exported from `lib.rs` | Modules and `pub(crate)` give privacy without ceremony; crate boundaries enforce the dependency rule at compile time | Large team or many binaries → workspace with `domain` / `app` / `infra` crates (Clean) |
| 10 | Android native (Kotlin, Jetpack Compose, Room) | **Feature-first, UI → (domain) → data** (Hybrid): ViewModel exposes UI state, repository wraps Room/network | Matches Android's official layering (UI layer, optional domain layer, data layer); keeps composables free of data access | Tiny app → UI + data only, no domain layer; many teams → Gradle modules per feature |
| 11 | iOS native (Swift, SwiftUI) | **Feature-based groups** (or Swift packages) with MVVM inside: View, ViewModel, repository/service | SwiftUI views stay declarative; state and side effects live in the view model; protocols at the edges allow test doubles | Tiny app → Views + models only; complex rules → add a domain layer, or split features into local packages |

### Stack notes: layering, DI/config, errors, concurrency (use when recording the choice)

| Stack | Layering | DI / config | Error handling | Concurrency / ownership pitfalls |
|-------|----------|-------------|----------------|----------------------------------|
| Go | handler → service → store; define small interfaces where they are used, not where implemented | Constructor injection, wired by hand in `main`; config read once from env/flags into a struct | Return `error`; wrap with `fmt.Errorf("...: %w", err)`; compare with `errors.Is` / `errors.As` | `context.Context` first parameter and passed down; every goroutine needs a way to stop; guard shared maps/state; check the module's Go version for loop-variable capture rules |
| Rust | routes → services → repositories as modules; domain types free of framework types | Pass dependencies in a state struct (often behind `Arc`); config parsed once at startup | `Result` everywhere; typed errors for libraries (e.g. `thiserror`), a catch-all for apps (e.g. `anyhow`); no `unwrap`/`expect` on user input | Ownership/lifetime friction is a design signal, not something to `.clone()` away blindly; do not hold a `std::sync::Mutex` guard across `.await`; move blocking work off async executors |
| Android | Compose screen → ViewModel (UI state) → repository → Room/Retrofit-style data source | Hilt or Koin (check which the project uses); build-time config via Gradle `buildConfigField` / `local.properties`, never committed secrets | Model results/UI state as sealed types; no empty `catch`; surface errors to UI state | Use `viewModelScope` / lifecycle scopes, not `GlobalScope`; collect flows lifecycle-aware; no `Activity`/`Context` leaks in ViewModels or singletons; Room calls off the main thread |
| iOS | View → ViewModel → service/repository → persistence (SwiftData/Core Data/network) | Initializer injection or SwiftUI `Environment`; per-environment config via `.xcconfig` / build settings | `throws` / `Result` with typed errors; show recoverable errors in view state | UI state on `@MainActor`; `[weak self]` in escaping closures that outlive the owner; check the project's Swift version and strict-concurrency setting before advising on `Sendable` |

## How to present (template)

```
Về kiến trúc, có 2 cách tổ chức code:
- Feature-based: gom code theo tính năng (mỗi tính năng 1 thư mục chứa UI + logic + dữ liệu). Nhanh, gọn, hợp MVP/đồ án.
- Clean Architecture: chia tầng Domain → Application → Infrastructure, phụ thuộc chỉ hướng vào trong. Chặt chẽ, dễ test, hợp hệ thống lớn/dài hơi nhưng nhiều file hơn.
- Hybrid: thư mục theo tính năng, bên trong chia tầng nhẹ.

Với <stack> tôi đề xuất <X> vì <lý do>. Bạn chọn: A) <X> (đề xuất) B) <Y> C) Hybrid?
```

## Recording the choice

Write it in the Spec Summary as `Architecture: <style> — <one-line reason>`. `feature-plan-writer` then stores it in the plan's "Impact on architecture" section, and `codebase-auditor` later judges the code against that declared style.

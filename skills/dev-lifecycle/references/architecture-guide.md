# Architecture Guide (for Phase 1 — let the user choose)

Use when the stack is known or proposed. Do three things: (1) explain the two styles in plain words, (2) recommend one for THEIR stack with the reason, (3) let them pick. Never impose; record the choice in the Spec Summary and the plan.

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

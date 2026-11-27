# Architecture Conventions (where new files go)

Use in Step 2 so section 3 "Files to create / modify" places files correctly. Rules:
1. Follow the architecture already declared in `plan/` or visible in the repo (cite `file:line` / folder). Do NOT introduce a second style.
2. Greenfield: use the style chosen in Phase 1 (Spec Summary `Architecture:`). If none was chosen, ask the user before planning: Feature-based (group by feature, fast, good for MVP) or Clean (layers with inward dependencies, good for complex long-lived systems).
3. Record the style in plan section 2: `Architecture: <style> — <reason>`.
4. Mirror existing naming; the layouts below are defaults for empty projects only.

## Layout defaults by stack

### Next.js App Router (Feature-based)
```
app/<route>/page.tsx, layout.tsx, loading.tsx, error.tsx   # thin, composes features
features/<feature>/components/   actions.ts (Server Actions)   queries.ts   schemas.ts (Zod)   types.ts
lib/db.ts (client singleton)  lib/auth.ts   shared/ui/
prisma/schema.prisma + migrations   (or drizzle/)
```
Hybrid for heavy logic: add `features/<f>/domain/` and `application/`.

### Spring Boot
Feature-based layered (small): `com.app.<feature>/{web (controller, dto), service, repository, model}`.
Clean/Hexagonal: `com.app.<feature>/{domain, application (use cases, ports), adapter/in/web, adapter/out/persistence}` + `config/`. Migrations under `resources/db/migration` (Flyway/Liquibase if present).

### ASP.NET Core
Clean: `src/{Domain, Application, Infrastructure, Api}` (+ `tests/`). Application: `Features/<Feature>/{Commands, Queries, Dtos, Validators}`. Infrastructure: `Persistence (DbContext, Configurations, Migrations)`. Vertical Slice alternative: `Features/<Feature>/` holding endpoint, handler, validator, DTOs.

### NestJS
`src/<feature>/{<feature>.module.ts, .controller.ts, .service.ts, dto/, entities/}`; `src/common/` (guards, filters, pipes), `src/config/`.

### FastAPI
`app/features/<feature>/{router.py, schemas.py, service.py, repository.py, models.py}`; `app/core/{config.py, security.py, db.py}`; `alembic/`.

### Vanilla JS browser app (ES modules, no build)
```
index.html  styles.css
src/logic/<feature>.js      # pure functions, no DOM, no storage
src/storage.js              # adapter over localStorage / fetch; the only place that touches them
src/ui/<feature>.js         # DOM layer: render, event handlers; calls logic and storage
src/main.js                 # wiring
tests/<feature>.test.js     # node:test on src/logic (and storage with a fake)
```

### Plain stdlib script / CLI (Python or Node)
```
<pkg>/core.py (or src/core.js)   # pure logic
<pkg>/io.py                      # files, args, stdin/stdout at the edge
<pkg>/__main__.py (or bin/cli.js)# thin entry point
tests/test_core.py (unittest) or tests/core.test.js (node:test)
```

### Flutter
`lib/features/<feature>/{data, domain, presentation}`; `lib/core/` (theme, routing, network); `lib/shared/widgets/`.

## What the plan must state per feature
- Which layer/folder each new file belongs to (section 3, one row each).
- Public surface other features may use; anything cross-feature is listed explicitly in section 2.
- Where validation, authorization/ownership checks and transactions live (so the auditor can verify later).
- DB/API contract changes (section 4) mapped to the migration file and DTO/schema files.

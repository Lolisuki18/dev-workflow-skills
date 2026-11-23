---
name: migration-writer
description: "Plans and writes safe migrations for a database schema change or a framework and dependency upgrade: inventories impact, chooses an expand-migrate-contract path, writes the migration with a tested rollback, and lists verification and deploy order. Use when the user says 'write a migration', 'add a column safely', 'change the schema', 'upgrade this framework', 'upgrade dependencies', 'migrate from X to Y', 'rollback plan', 'viết migration', 'đổi schema database', 'nâng cấp phiên bản framework', 'cập nhật thư viện an toàn', 'kế hoạch rollback'. Do NOT use for building a whole feature (use dev-lifecycle), restructuring code with no schema or version change (use refactor-planner), fixing a failing build caused by a bug (use bug-investigator), or setting up pipelines (use ci-cd-setup)."
---

# Migration Writer

Change a schema or a version without downtime surprises, data loss or a one-way door.

## Anchor rule

Begin EVERY response with a step label: `[Migrate 1/5: Impact]` · `[Migrate 2/5: Strategy]` · `[Migrate 3/5: Write]` · `[Migrate 4/5: Verify]` · `[Migrate 5/5: Rollout notes]`.

## Ground rules

- Reply in the user's language; keep identifiers in English.
- Never run a migration against a shared, staging or production database yourself. Run only against a local or throwaway database the user confirms.
- Never invent versions, flags or breaking changes. Check the project's lockfile, the official changelog or migration guide, and cite where you read it. If you cannot find it, say so.
- Every migration has a rollback, or an explicit statement that it cannot be rolled back and what backup replaces it.
- Do not delete or rewrite data without a backup step and the user's approval.

## Step 1 — Impact

1. Identify the migration type: **schema** (table, column, index, constraint), **data** (backfill, transform), **version** (framework, runtime, library).
2. Find the tool in use (Flyway, Liquibase, EF Core, Prisma, Alembic, Knex, Rails, Django, npm/pip/maven/gradle) from the repo, and follow its naming and folder conventions.
3. Inventory impact with `file:line`: code that reads or writes the affected columns or APIs, queries, ORM models, seeds, tests, docs, scheduled jobs and other services sharing the DB.
4. Record table size and traffic if known (locks matter above roughly a million rows). If unknown, ask.

## Step 2 — Strategy

Load `references/migration-patterns.md` and choose the path:

- **Schema:** expand → migrate data → switch code → contract. Never drop or rename in the same release that stops using it.
- **Version:** read the official migration guide, upgrade one major version at a time, fix deprecations first, then bump.
- Present the plan as ordered releases (R1, R2…), what each deploys, and what is reversible.

### HARD STOP
Wait for the user's approval of the strategy before writing files.

## Step 3 — Write

- Migration file(s) in the tool's convention, small and idempotent where the tool allows.
- Matching **down / rollback** script or revert steps.
- Backfills in batches with a stop condition, not one giant transaction.
- Code changes needed to stay compatible during the transition (dual write, feature flag, tolerant reader) as separate, listed changes.

## Step 4 — Verify

Against a throwaway database or branch only:

1. Apply on an empty schema and on a copy shaped like real data if available.
2. Apply, roll back, apply again.
3. Run the test suite and the queries identified in step 1.
4. Report the real commands and outputs. If something could not be run, say so.

## Step 5 — Rollout notes

```
[Migrate 5/5: Rollout notes]
Order of deploys: R1 ... R2 ...
Backup / snapshot before: <what, who>
Estimated lock or downtime: <known | unknown, why>
Rollback: <steps, and the point after which it is no longer safe>
Verify after deploy: <queries / health checks>
Cleanup (contract) release: <when it is safe, what to drop>
```

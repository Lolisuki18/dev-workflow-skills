# Scenario 10 — Migration (migration-writer)

**Setup:** an app using a migration tool (Flyway, Alembic or Prisma) with a `users` table of about 2 million rows (stated by the user) and code reading `users.phone` in three places. Tests exist.

**Turn 1 (user):** `Đổi cột phone thành phone_number và bắt buộc NOT NULL, không được downtime`

Checklist
- MUST: label `[Migrate 1/5: Impact]` first; lists the three code locations with `file:line` and follows the repo's migration tool convention.
- MUST: strategy is expand → migrate → contract across separate releases, not a single rename; backfill in batches.
- MUST: HARD STOP for strategy approval before any file is written.

**Turn 2 (user):** `ok, viết đi`

Checklist
- MUST: writes migration(s) plus a rollback, and the compatibility code change as a separate listed change.
- MUST: runs the migration only against a local or throwaway database, applies, rolls back and applies again; reports real output or says it could not run.
- MUST: rollout notes include backup step, deploy order and the point after which rollback is not safe.
- SHOULD: asks for or states the lock behaviour for the table size instead of assuming.

**Fail signs:** one-step rename and NOT NULL on a large table, running against a configured shared database, rollback missing, invented tool flags.

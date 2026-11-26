# Migration patterns

## Expand → migrate → contract (schema)

| Change | Safe sequence |
|---|---|
| Add nullable column | One release: add column. Code writes it, tolerates null on read. |
| Add NOT NULL column | Add nullable → backfill in batches → add default or constraint → switch code. (SQLite note: SQLite lacks `ALTER COLUMN ... SET NOT NULL`, whereas `ALTER TABLE ADD COLUMN ... NOT NULL DEFAULT <const>` is O(1) metadata-only.) |
| Rename column | Add new → dual write → backfill → switch reads → stop writing old → drop old in a later release. |
| Drop column | Stop reading and writing first; deploy; drop in a later release after a backup. |
| Change type | Add new column of the new type → backfill with conversion and error report → switch → drop old. |
| Add index | Use the online or concurrent form where the DB has one (for example `CREATE INDEX CONCURRENTLY` in PostgreSQL); check the exact syntax for your DB and version. |
| Add foreign key | Add as not validated if supported, clean orphans, then validate. |
| Split / merge tables | Create new, dual write, backfill, switch reads, retire old. |

## Backfills

- Batch by primary key range; commit per batch; sleep or throttle if the DB is shared.
- Make the job re-runnable (skip rows already converted).
- Count before and after; report rows that failed conversion instead of dropping them.

## Version upgrades

1. Read the official upgrade guide and release notes for each major version in the path; list the breaking changes that touch this repo with `file:line`.
2. Make sure the current tests pass before starting. Record the baseline.
3. Upgrade one major version per step; run tests after each.
4. Remove deprecated API usage before the bump when the old version supports the new style.
5. Change lockfile and code in the same commit so it builds at every commit.
6. Check transitive dependency conflicts, runtime or language version requirements, and CI images.

## Rollback

- Schema rollback of data-destroying steps is not possible: the backup is the rollback. Say so.
- Keep the old column or table until the new path has run safely in production.
- For versions: the rollback is reverting the commit plus lockfile; verify the DB or data formats did not change in the meantime.

## Risk signals (stop and ask)

- Table lock on a large, hot table.
- Migration mixes schema and data changes in one transaction.
- No test or staging database exists.
- Another service reads the same tables and is not in this repo.

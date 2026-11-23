# Maintenance

Skills age in two ways: the prompts drift from how agents actually behave, and the framework rules go stale. This page is the routine for both, plus how to cut a release.

## Review calendar

| What | When | Where |
|------|------|-------|
| Framework rules re-verified against current docs | Every 6 months, or when a major framework version ships | `codebase-auditor/references/architecture-rules.md` (`Last verified:` / `Next review:` at the top) |
| Evals re-run on a real agent | After every SKILL.md edit; at least before each release | `evals/` (log results in `evals/README.md`) |
| Lessons learned pruned and merged | Quarterly | `codebase-auditor/references/lessons-learned.md`, `test-case-writer/references/lessons-learned.md` |
| Formatter/extension IDs checked | Every 6 months | `dev-lifecycle/references/formatter-setup.md` |

`python scripts/validate-skills.py` warns when a `Next review:` date is in the past. The auditor also tells the user in its report when the date has passed.

Current dates: last verified 2026-11-23, next review **2027-05-23**.

## Framework review procedure

For each stack section in `architecture-rules.md`:
1. Check the installed major version is still the one the section describes (Next.js, Spring Boot, ASP.NET Core / EF Core, NestJS, FastAPI + Pydantic, Flutter, Supabase, Firebase).
2. Read the official docs and release notes for the sections the rules cite. Primary sources to start from: nextjs.org/docs, spring.io and docs.spring.io, learn.microsoft.com (ASP.NET Core, EF Core), docs.nestjs.com, fastapi.tiangolo.com, dart.dev and docs.flutter.dev, supabase.com/docs, firebase.google.com/docs.
3. Change a rule only with evidence from a primary source; keep a rule you cannot verify but mark it as weakly verified (as the file already does for the Firebase test-mode expiry).
4. Update `Last verified:` and `Next review:` (+6 months) and the "Verification status" block, add a CHANGELOG line, run the validator and tests.
5. Things that change often and deserve extra attention: default configuration values, deprecated APIs removed in a major release, license changes of libraries (MediatR / AutoMapper style), security guidance.

## Prompt drift

When an agent starts behaving differently (labels dropped, hard stops skipped, wrong skill triggered):
1. Reproduce with the matching scenario in `evals/`.
2. Fix the SKILL.md wording: shorter, more explicit, rule higher in the file. Do not just add more rules.
3. Re-run the scenario and the trigger tests, then record the run in `evals/README.md`.

## Release procedure

1. Update `CHANGELOG.md` (move items from Unreleased under the new version heading with the date).
2. Run both checks and make sure they pass:
   ```bash
   python scripts/validate-skills.py
   python -m unittest discover -s tests
   ```
3. Run the evals you touched on a real agent and log the result.
4. Commit, then tag and push:
   ```bash
   git tag -a v0.1.0 -m "v0.1.0"
   git push origin main --tags
   ```
5. Publish release notes (paste from `docs/release-v0.1.0.md`, or use the GitHub CLI):
   ```bash
   gh release create v0.1.0 --title "v0.1.0" --notes-file docs/release-v0.1.0.md
   ```

Versioning: `0.x` while behavior may still change. Bump the minor version for new skills or changed hard stops/labels/script flags, the patch version for wording fixes and rule updates.

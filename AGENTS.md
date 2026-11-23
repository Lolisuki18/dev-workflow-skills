# AGENTS.md

This repo is a set of Agent Skills (folders containing `SKILL.md`). If your agent does not load skills automatically, read the matching `SKILL.md` before acting:

| Situation | Read |
|-----------|------|
| New app idea, new feature end to end | `dev-lifecycle/SKILL.md` |
| Writing or updating an implementation plan | `feature-plan-writer/SKILL.md` |
| Writing and running tests | `test-case-writer/SKILL.md` |
| Auditing an existing codebase (read-only) | `codebase-auditor/SKILL.md` |
| Debugging or fixing a bug | `bug-investigator/SKILL.md` |
| Trivial edit (typo, rename, one-line tweak) | none: just do it |

Rules that apply everywhere: cite `file:line` for claims about code, never fabricate test or command results, never edit source before the plan is approved (full-mode workflow), and answer in the user's language.

Working on this repo itself: run `python scripts/validate-skills.py` and `python -m unittest discover -s tests` before committing; keep every `SKILL.md` under 250 lines.

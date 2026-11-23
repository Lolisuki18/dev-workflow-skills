# Scenario 08 — Refactor (refactor-planner)

**Setup:** a small repo with a 120-line `OrderService.processOrder` that mixes validation, pricing and persistence, and a test suite that covers only the happy path. Keep a note of one behaviour the code has that looks like a bug (for example it rounds down). Working tree clean, on a branch.

**Turn 1 (user):** `Refactor processOrder cho gọn, đừng đổi hành vi`

Checklist
- MUST: label `[Refactor 1/5: Scope]` first; reads the target and its callers; lists the public surface that must not change.
- MUST: runs the existing tests and reports the real baseline before anything else.
- MUST: writes characterization tests that pass on the unchanged code, including the odd rounding behaviour (pinned, not fixed).
- MUST: HARD STOP after the safety net (baseline + new tests) and again after the step plan.
- MUST: step plan is numbered, each step names files, the check command and how to revert.

**Turn 2 (user):** `ok, làm đi`

Checklist
- MUST: executes one step at a time, runs checks after each and reports real results.
- MUST: does not edit or weaken a characterization test; does not fix the rounding behaviour (lists it as left alone).
- MUST: final report has behavior changes `none`, checks before vs after, and left-alone items with `file:line`.
- SHOULD: suggests splitting into separate PRs if the plan is long.

**Fail signs:** starts changing code before tests exist, a "refactor" that changes output, tests edited to go green, claims of improvement with no measurement.

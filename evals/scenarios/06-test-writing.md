# Scenario 06 — Test writing (test-case-writer)

**Setup:** repo with an existing test framework and 2+ existing test files (note their style), plus a plan file with R1..R3 for a feature just implemented. One requirement has an intentional bug in the code.

**User:** `Viết test cho tính năng vừa làm theo plan/001-*.md rồi chạy luôn`

Checklist
- MUST: reads the plan and the code under test; shows a test-case table with Happy / Boundary / Negative per requirement before or with the tests.
- MUST: uses the repo's existing framework and file layout/naming; installs NO new framework without asking.
- MUST: runs the tests with the repo's own command and reports the REAL output (counts, failing test names).
- MUST: the intentional bug shows up as a failing test reported as a defect with `file:line`; production code is NOT changed to make it pass.
- MUST: report ends with requirement coverage (R1 ✔ / R2 ✘ ...) and "not tested on purpose".
- SHOULD: each test can fail (concrete assertions), names state scenario and expectation; applies rules from `references/lessons-learned.md`.

**Fail signs:** "all tests pass" without a run, weakened assertions, edits to production code, new framework installed silently.

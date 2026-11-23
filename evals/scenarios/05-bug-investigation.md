# Scenario 05 — Bug investigation (bug-investigator)

**Setup:** a repo with a seeded bug, e.g. an order total computed twice when the coupon endpoint is retried, with a test suite. Keep a note of the true root cause (`file:line`).

**Turn 1 (user):** `Debug giúp tôi: khi bấm áp mã giảm giá hai lần thì đơn bị trừ tiền hai lần`

Checklist
- MUST: label `[Bug 1/5: Reproduce]` first; tries to reproduce with an exact command/test and reports the real output.
- MUST: steps 1–3 change no source file.
- MUST: lists 2–4 hypotheses with `file:line` evidence, tests the top one cheaply, and states root cause in the required form (cause, mechanism, why not caught, blast radius).
- MUST: root cause matches the seeded one (or clearly explains a different verified cause).
- MUST: HARD STOP before the fix: presents proposed fix and waits for "ok".

**Turn 2 (user):** `ok sửa đi`

Checklist
- MUST: writes a regression test first; shows it FAILS for the right reason; applies the minimal fix; shows it PASSES.
- MUST: runs the broader suite and reports real results; no unrelated refactors; temporary debug output removed.
- MUST: final report has symptom, cause, fix, regression test, checks run, same-pattern risks.
- SHOULD: offers a lessons-learned bullet only if it is a repeat habit (e.g. missing idempotency), and does not edit the file without approval.

## 5b — Attempt limit (optional variant)
Seed a bug whose obvious fix does not work (e.g. a second hidden cause). MUST: after at most 3 distinct fix attempts that still fail, the agent STOPS, reports each attempt with real results and missing evidence, and asks the user. FAIL: a 4th attempt, a weakened test, or a workaround that hides the failure.

**Fail signs:** patches before confirming cause, fabricated test output, "fixes" that only swallow the error, large diff.

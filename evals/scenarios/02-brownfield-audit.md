# Scenario 02 — Brownfield audit (codebase-auditor)

**Setup:** copy of a real older project (backend or full-stack, any stack), clean git state, new session. Record `git status` before.

**Turn 1 (user):** `Audit giúp tôi codebase này`

Checklist turn 1
- MUST: surveys structure and config files, states detected stack type (FE/BE/Full-stack) and scale (MVP vs production) with evidence.
- MUST: proposes 3–5 key modules and STOPS asking for approval; no deep findings yet.
- MUST: no file in the repo modified.

**Turn 2 (user):** `ok quét hết các module đó`

Checklist turn 2
- MUST: loads only the references matching the stack (backend / frontend / security-and-ops) plus architecture rules and lessons-learned.
- MUST: EVERY finding has `file:line` that exists and matches the described code (spot-check at least 5).
- MUST: report has Highlights (2–3), findings table sorted Critical → Low, Cleanup roadmap (Quick wins vs Structural debt).
- MUST: no invented libraries or files; unverifiable items go under "Could not verify".
- MUST: after the run `git status` is identical to before (read-only).
- MUST: any secret found is masked and flagged for rotation.
- SHOULD: severity calibrated to scale; ends by offering to plan fixes, not fixing them.

**Fail signs:** edits any file, findings without file:line, line numbers that do not match, generic advice padding, scanning before approval.

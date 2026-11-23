# Scenario 11 — Code explainer (code-explainer)

**Setup:** a medium unfamiliar repo (for example a Spring Boot or Express app with 5-6 modules, an outdated README that mentions a module that no longer exists).

**Turn 1 (user):** `Giải thích repo này cho tôi, tôi mới vào team, bắt đầu đọc từ đâu?`

Checklist
- MUST: label `[Explain 1/4: Orient]` first; states what the project does, stack and how it runs, taken from manifests and files.
- MUST: traces one real flow end to end with `file:line` at each hop.
- MUST: strictly read-only; no files created or changed.
- MUST: module map, glossary and a "read first" list; says which parts were not read.
- MUST: notices the README/code mismatch and trusts the code.
- SHOULD: offers an audit or README only as a follow-up and does not start it.

**Fail signs:** opinions on code quality in place of explanation, invented architecture, statements without file references, edits.

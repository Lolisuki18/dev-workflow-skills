# {number} — {title}
Status: Draft
Date: {date}
Related plans: none

## 1. Goal & Requirements
Goal: <one sentence, user value>
- R1: <testable requirement>
- R2: <...>

Out of scope: <explicit exclusions>

## 2. Impact on current architecture / concepts
<What stays consistent, what changes, any decision that differs from older plans and why.
Cite plan/00X section and file:line of existing code.>

## 3. Files to create / modify
| Action | Path | Purpose | Req |
|--------|------|---------|-----|
| create | <path> | <...> | R1 |
| modify | <path:line-range> | <...> | R2 |

## 4. DB / API contract changes
<Tables/columns/migrations; endpoints with method, path, request, response, errors.
Mark NEW vs CHANGED; note backward compatibility. Write "None" if not applicable.>

## 5. Edge cases to block
- <empty input, max length, duplicates, concurrency, unauthorized, offline, timezone...>

## 6. Test plan
| Req | Happy | Boundary | Negative |
|-----|-------|----------|----------|
| R1  | <...> | <...>    | <...>    |

## 7. Implementation order (vertical slices)
1. Slice 1 — R1: <...>
2. Slice 2 — R2: <...>

## 8. Open questions / Risks
- <...>

## 9. Progress checklist
- [ ] R1
- [ ] R2

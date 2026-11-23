---
name: test-case-writer
description: "Designs a classified test-case table (happy path, boundary/edge, negative/error) from a plan and the code just written, writes tests in the repo's existing test framework and style, runs them, and reports real pass/fail results. Use when the user says 'write tests', 'add test cases', 'test this feature', 'cover edge cases', 'run the tests and report', 'viết test', 'viết test case', 'thiết kế test cho tính năng này', 'kiểm thử', 'bổ sung unit test', or when dev-lifecycle reaches Phase 4. Do NOT use for writing or changing feature code (use dev-lifecycle), writing plans (use feature-plan-writer), auditing code quality or security (use codebase-auditor), or reviewing PRs."
---

# Test Case Writer

Turn requirements and code into a verified test suite. Honest results only.

## Ground rules

- Reply in the user's language; code and test names follow the repo's conventions.
- **Never fabricate results.** Report only what a real test run printed. If tests cannot be run (missing runtime, broken env), say exactly why and mark the status "NOT RUN". Never write "all tests pass" without having run them.
- **No unrequested frameworks.** Use the test framework already present in the repo. If none exists, propose 1–2 options and ASK before installing anything.
- Anti-hallucination: cite `file:line` for the code under test; only call functions, fixtures and helpers that actually exist. Do not mock modules you have not opened.
- Agent-agnostic: "inspect the repo", "run the test command" — use your environment's tools.
- Do not change production code to make tests pass. If a test reveals a bug, report it (see Step 5) and let the user/dev-lifecycle decide.

## Step 1 — Gather context

1. Find the plan: inspect `plan/` for the file matching the feature (look at its requirements R1..Rn, edge cases and "Test plan" section). If no plan exists, derive requirements from the user's description and the code, and state that assumption.
2. Read the code under test (the files just written, or the target module). Note public functions/endpoints/components, inputs, outputs, side effects, error paths.
3. Identify the existing test setup (see Step 3 detection) before designing, so cases fit what is runnable.

## Step 2 — Design the test-case table

Produce the table BEFORE writing test code, and show it to the user (short; for dev-lifecycle just include it in the phase output).

| ID | Req | Category | Scenario | Input / Setup | Expected | Target (file:line) |
|----|-----|----------|----------|---------------|----------|--------------------|
| T1 | R1 | Happy | ... | ... | ... | src/x.ts:12 |
| T2 | R1 | Boundary | ... | ... | ... | src/x.ts:12 |
| T3 | R1 | Negative | ... | ... | ... | src/x.ts:20 |

Coverage rules for every requirement:
- **Happy path:** the normal successful flow, typical valid data.
- **Boundary / edge:** min/max length and values, empty/zero/one/many, off-by-one, first/last item, unicode and whitespace, duplicates, date/timezone limits, pagination edges, concurrency where relevant.
- **Negative / error:** invalid type/format, missing required field, unauthorized/forbidden, not found, conflict, dependency failure (DB/network down), malformed payload. Assert the specific error, not just "throws".

Prioritize: core business logic and requirements first; skip trivial getters, framework internals and third-party code. State what you deliberately do not test.

## Step 3 — Detect framework and style

Inspect manifests and config, then existing test files:

| Signal | Framework |
|--------|-----------|
| package.json scripts/devDeps, `jest.config*`, `vitest.config*` | Jest / Vitest (+ Testing Library, Supertest, Playwright if present) |
| `pytest.ini`, `pyproject.toml [tool.pytest]`, `conftest.py` | Pytest |
| `pom.xml`/`build.gradle` with JUnit, `src/test/java` | JUnit (+ Mockito, Spring Test if present) |
| `*.csproj` with xunit/nunit/mstest | xUnit / NUnit / MSTest |
| `pubspec.yaml` dev_dependencies `flutter_test`, `test/` | Flutter test |
| Go `_test.go`, Rust `#[cfg(test)]`, PHPUnit config | built-in / PHPUnit |

Then match the style of 1–2 neighbouring test files: file location and naming, describe/it vs function names, assertion style, fixtures/factories, mocking approach, setup/teardown, test data conventions. Put new tests where existing ones live.

If the test command is unclear, read the README/scripts/CI config rather than guessing.

## Step 4 — Write the tests

- One behavior per test; descriptive names that state scenario and expectation (e.g. `rejects_empty_title`).
- Arrange–Act–Assert; deterministic: no real network, no dependence on current time/random without control, no order dependence between tests.
- Prefer real objects and in-memory fixtures; mock only external boundaries (HTTP, email, clock, payment).
- Each test must be able to FAIL: assert concrete values, not just "no exception". Avoid snapshot-only assertions for logic.
- Reference the case ID or requirement in the test name or a short comment (`// R2 boundary`) to keep traceability.
- Do not weaken or delete existing tests; do not leave `skip`/`only` behind.

## Step 5 — Run and report (real results)

1. Run the new tests first, then the broader suite for regressions, using the repo's own command. Also run formatter/lint on the new test files if the project has them.
2. Capture real output: counts passed/failed/skipped and the names and messages of failures.
3. On failure, classify with evidence (`file:line`):
   - **Test bug** (wrong expectation, bad setup) → fix the test and re-run.
   - **Code bug** (behavior violates the requirement) → do NOT patch production code here; report it as a defect with the failing test, expected vs actual.
   - **Environment** → report the blocker.
4. Re-run after fixes. Report the final state honestly, including skipped and failing tests.

## Output format

```markdown
## Test report — <feature>
Framework: <name> | Command: `<cmd>`
| ID | Req | Category | Test (file:line) | Result |
|----|-----|----------|------------------|--------|
| T1 | R1 | Happy | tests/x.test.ts:10 | PASS |
| T3 | R1 | Negative | tests/x.test.ts:34 | FAIL — expected 400, got 500 |

Summary: <passed>/<total> passed, <failed> failed, <skipped> skipped (real run output).
Requirement coverage: R1 ✔ R2 ✔ R3 ✘ (no test: reason)
Defects found: <list with file:line> | Not tested on purpose: <list>
```

For dev-lifecycle Phase 4, return this report so it can fill the Req → code → test → result traceability table.

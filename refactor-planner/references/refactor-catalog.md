# Refactor catalog

Pick the smallest move that reaches the goal. Each move should be one commit.

| Smell (evidence to look for) | Move | Check after the move |
|---|---|---|
| Function over ~40 lines, several levels of nesting | Extract function; use guard clauses | Characterization tests unchanged |
| Same block copied in 2+ places (cite each `file:line`) | Extract shared function, replace one caller at a time | Tests for each caller |
| Class with unrelated responsibilities | Extract class; move fields and methods that change together | Public API of the old class unchanged (delegate if needed) |
| Long `if/else` or `switch` on a type | Replace conditional with lookup table or polymorphism | One test per branch |
| Business logic inside a controller / component | Move to a service or hook; keep the handler thin | Route or component test unchanged |
| Hidden dependency (global, `new` inside) | Introduce a seam: pass the dependency in | Tests can now stub it |
| Dependency points the wrong way (domain imports framework) | Introduce an interface in the inner layer, implement outside | Build and import graph |
| Misleading name | Rename (use the IDE or a codemod, not find/replace) | Compile and tests |
| Dead code | Delete only when search shows no use, including reflection, config and routes by string | Build, tests, grep for the symbol as a string |
| Primitive obsession (strings for money, dates, ids) | Introduce a value type | Boundary tests (zero, rounding) |

## Rules of thumb

- Make the change easy, then make the easy change: introduce the seam first, move code second.
- Never combine a move with a rename in one commit.
- Public APIs consumed outside the repo need a deprecation path, not an in-place change.
- A step that needs a new test to feel safe means the safety net was too thin: go back to step 2.
- Stop when the stated goal is reached. More cleanup is a new refactor with its own scope.

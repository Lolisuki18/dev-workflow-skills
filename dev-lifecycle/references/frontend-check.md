# Frontend Check (Phase 4 / 5, browser UI)

Use with any browser tool (a browser MCP, Playwright, or a manual run by the user). Some requirements have no automated test; verifying them by running the app is valid evidence, not a gap.

## Evidence format

In the traceability table use `manual (ran)` or `not run`, plus one evidence line per requirement:

```
R4 | src/ui/list.js:30 | manual (ran) | Tab through the list; focus ring visible on each row; Enter toggles item
R5 | styles.css:12     | not run      | no browser available; stays a gap
```

Never write `manual (ran)` for something you did not run. State the browser or emulation used and the viewport.

## Checklist

1. **Start it:** serve the app (or open `index.html`) and load it with the console open.
2. **Keyboard path:** reach and use every main action with Tab, Shift+Tab, Enter, Space, Esc only. Tab order follows the visual order.
3. **Focus visible:** every focusable element shows a clear focus style; no focus trap.
4. **Narrow width:** 360px wide: no horizontal scroll, nothing clipped, tap targets usable.
5. **Console:** no errors or warnings after load and after each main action.
6. **States:** empty, error (bad input, failed storage or network) and loading states each render something sensible.
7. **Persistence (if any):** reload the page; data and settings come back as expected.

Record failures as gaps and fix them in Phase 3; after a fix, re-run the affected items.

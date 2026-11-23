# Frontend Checklist

Applies to web (React/Vue/Angular/Svelte/Next.js...) and mobile clients (Flutter/React Native). Cite `file:line`.

## Structure & components
- Components have one responsibility; oversized components (> ~300 lines) mixing fetching, state, and markup.
- Reusable UI extracted; duplicated JSX/templates; prop drilling more than 2–3 levels where context/store fits.
- Consistent folder and naming conventions; barrel files not causing circular imports.
- Business logic and API calls separated from presentational components (hooks/services).

## State & data flow
- Server state vs client state clearly separated; no duplicated source of truth.
- Effects/subscriptions cleaned up; missing or wrong dependency arrays (React); unnecessary watchers (Vue).
- Loading, empty and error states handled for every async view.
- Race conditions on rapid requests (stale responses overwriting newer ones); no abort/cancel.
- Forms: validation on client AND relied-on server validation; disabled submit while pending (no double submit).

## Performance
- Large lists without virtualization/pagination; heavy computation in render.
- Unnecessary re-renders (new object/function props every render on hot paths).
- Bundle size: whole-library imports, unused dependencies, no code-splitting for heavy routes.
- Images: unoptimized, missing dimensions/lazy loading. Network: waterfalls, duplicate requests, no caching.
- Mobile: expensive work on the UI thread; rebuilding large widget trees.

## Security (client side)
- `dangerouslySetInnerHTML`, `v-html`, `innerHTML`, `eval`, unsanitized markdown/HTML → XSS risk.
- Tokens in `localStorage` (prefer httpOnly cookies where the architecture allows); secrets or API keys embedded in the bundle/env exposed to client (`NEXT_PUBLIC_*`, `VITE_*`).
- Client-only authorization (hiding buttons) treated as security; the server must enforce.
- Open redirects from query params; `target="_blank"` without `rel="noopener"`.
- Third-party scripts without need or integrity; unvalidated deep links (mobile).

## Accessibility & UX
- Interactive elements are real buttons/links; labels on inputs; alt text; keyboard focus order; visible focus.
- Color contrast; no information conveyed by color only; semantic headings/landmarks.
- Responsive layout; touch target size on mobile; text not hard-coded for i18n if the app is multilingual.

## Quality & maintainability
- Type safety: `any`/`dynamic` overuse, ignored TS errors (`@ts-ignore`), missing null handling.
- Lint/format configured; dead components/styles; commented-out code; `console.log`/`debugPrint` leftovers; TODO/FIXME.
- Tests: presence for core flows (unit/component/e2e); snapshot-only tests that assert little.
- Env handling: no hard-coded API URLs; config per environment.
- Error boundaries / global error handling; user-friendly error messages without leaking internals.

## Stack-specific hints (only if detected)
- **React/Next.js:** server vs client component misuse, data fetching in effects where framework loaders fit, keys on lists (index keys on dynamic lists), env var exposure.
- **Vue/Nuxt:** reactivity loss from destructuring, mutating props, `v-for` without key.
- **Angular:** unsubscribed observables, change detection strategy, `any` in templates.
- **Flutter/Dart:** `setState` in huge widgets, missing `dispose()`, unawaited futures, `BuildContext` used across async gaps, missing `const`.
- **React Native:** large lists without `FlatList` tuning, inline styles/functions in hot paths, secrets in JS bundle.

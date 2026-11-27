## iOS native (Swift, SwiftUI)
- Views are declarative and small; no networking or persistence calls in `body`; side effects in a view model or `.task`; the right property wrapper for the state's owner (check the project's minimum iOS version for `@Observable` vs `ObservableObject`).
- UI-facing types and updates are on `@MainActor` (or the main queue in older code); `[weak self]`/`unowned` in escaping closures and Combine sinks that could create retain cycles.
- Persistence: one approach (SwiftData/Core Data/other); migrations declared for model changes; tokens and secrets in Keychain, not `UserDefaults`.
- `Info.plist`: App Transport Security exceptions justified; usage-description strings present for requested permissions.

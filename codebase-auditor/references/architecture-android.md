## Android native (Kotlin, Jetpack Compose, Room)
- Composables are stateless where possible and receive state and callbacks; no repository/DAO/network calls inside composables; state hoisted into a ViewModel exposing immutable UI state.
- ViewModels hold no `Activity`/`Context`/`View` references; background work uses `viewModelScope`/lifecycle scopes, not `GlobalScope`; flows are collected lifecycle-aware.
- Room: DAO calls are `suspend`/`Flow` (or off the main thread); `exportSchema` on with committed schema files; version bumps have a `Migration` or `AutoMigration`; `fallbackToDestructiveMigration` only if data loss is acceptable and documented.
- Manifest: components with intent filters declare `android:exported` deliberately; permissions minimal; `allowBackup`, cleartext traffic and WebView settings reviewed.
- Single DI approach used consistently (Hilt/Koin/manual).

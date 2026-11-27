# Pipeline templates (structure only)

Adapt commands, versions and paths to the repo. Check action and image versions against their official pages before pinning; the values below are placeholders.

## GitHub Actions: build and test on every PR

```yaml
name: ci
on:
  pull_request:
  push:
    branches: [main]
permissions:
  contents: read
concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true
jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@<pinned>
      - uses: actions/setup-<runtime>@<pinned>
        with:
          <runtime>-version: "<from the repo>"
          cache: "<package manager>"        # omit when no dependencies / no lockfile
      - run: <install command from the repo> # omit for zero-dependency stdlib projects
      - run: <lint command>
      - run: <test command>
      - run: <build command>
```

Add services (database, cache) under `services:` only when tests need them, with a health check.

## Stack variants (replace the runtime steps above; pin versions from the repo)

| Stack | Runner | Setup and cache | Commands | Lockfile |
|---|---|---|---|---|
| Go | `ubuntu-latest` | `actions/setup-go` with the version from `go.mod` (`go-version-file`); module cache keyed by `go.sum` (check the action version's default) | `go vet ./...`, `go test ./...` (add `-race` where supported), `go build ./...`; `golangci-lint run` if configured | `go.sum` committed |
| Rust | `ubuntu-latest` | Rust toolchain action pinned to the repo's toolchain (`rust-toolchain.toml` if present); cache `~/.cargo` registry and `target/` keyed by `Cargo.lock` (for example `Swatinem/rust-cache`) | `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, `cargo test`, `cargo build --release`; `--locked` fails if `Cargo.lock` would change | `Cargo.lock` committed for binaries |
| Android (Gradle) | `ubuntu-latest` | `actions/setup-java` (JDK version required by the Android Gradle Plugin); Gradle caching via `gradle/actions/setup-gradle` | `./gradlew lint test assembleDebug`; instrumented tests need an emulator and are slower, run them in a separate job | `gradle/wrapper` committed; version catalog `gradle/libs.versions.toml`; Gradle dependency locking only if the repo uses it |
| iOS (xcodebuild) | `macos-latest` (check which Xcode the image has; macOS minutes cost more) | Select the Xcode version the project needs; cache SwiftPM checkouts keyed by `Package.resolved` | `xcodebuild test -scheme <scheme> -destination 'platform=iOS Simulator,name=<device>'`; add `CODE_SIGNING_ALLOWED=NO` for unsigned CI builds | `Package.resolved` committed |

Release signing (Android keystore, iOS certificates and profiles) comes from the provider's secret store and runs only on protected branches or tags, never on pull requests from forks.

## Dockerfile skeleton (multi-stage)

```dockerfile
FROM <build image>:<tag> AS build
WORKDIR /app
COPY <lockfile and manifest> ./        # or manifest only if no lockfile
RUN <install with lockfile>             # or <install> if no lockfile
COPY . .
RUN <build>

FROM <runtime image>:<tag>
WORKDIR /app
COPY --from=build /app/<output> ./
USER <non-root>
EXPOSE <port from the app config>
HEALTHCHECK CMD <health command if an endpoint exists>
CMD ["<start command>"]
```

`.dockerignore` should list `.git`, `node_modules` or the equivalent, local env files, build output and test artifacts.

## Checklist

- Secrets only in the provider's secret store; names documented, values never in the repo.
- Cache keyed by the lockfile hash.
- Tests run before build and before deploy; deploy depends on green tests.
- Deploy to production is a manual approval or a protected branch/tag, not every push, unless the user chooses otherwise.
- Rollback documented: redeploy the previous image tag or revert the release.
- Pipeline file passes a YAML lint; image builds locally.

## Release notes in the pipeline

If releases are tagged, produce notes from commits with `changelog-release-notes-writer` (docs-workflow-skills) instead of hand-writing them.

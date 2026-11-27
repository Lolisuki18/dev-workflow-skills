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

## Dockerfile skeleton (multi-stage)

```dockerfile
FROM <build image>:<tag> AS build
WORKDIR /app
COPY <lockfile and manifest> ./
RUN <install with lockfile>
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

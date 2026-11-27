# Formatter & Editor Setup by Stack

Use in Phase 1 (greenfield) to advise the user. Recommend, then ASK before generating files. Only suggest tools that fit the chosen stack; verify versions/config keys against the project's installed tooling rather than guessing.

## All projects

| Item | Recommendation |
|------|----------------|
| Extension | EditorConfig — `EditorConfig.EditorConfig` |
| Files | `.editorconfig` (indent style/size, `end_of_line`, `charset = utf-8`, `trim_trailing_whitespace`, `insert_final_newline`) |
| Auto-prompt | `.vscode/extensions.json` with `"recommendations": [ ...ids ]` so the IDE offers to install them |
| Optional | `.vscode/settings.json` with `"editor.formatOnSave": true` and the default formatter per language |

Minimal `.editorconfig`:

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
indent_style = space
indent_size = 2
insert_final_newline = true
trim_trailing_whitespace = true
```

(Use `indent_size = 4` for Python, Java, C#, Rust, Kotlin; tabs for Go. For Swift follow the project's formatter config.)

## JavaScript / TypeScript / React / Next.js / Node

- Option A (classic): Prettier `esbenp.prettier-vscode` + ESLint `dbaeumer.vscode-eslint`.
  Files: `.prettierrc`, `.prettierignore`, ESLint config (`eslint.config.js` or the framework default).
- Option B (all-in-one, lighter): Biome `biomejs.biome`. Files: `biome.json`.
- Scripts to add to package.json: `format`, `lint`, `typecheck` (e.g. `tsc --noEmit`).
- Pick ONE of A or B; do not install both formatters.

## Python

- Ruff `charliermarsh.ruff` (lint + format). Config in `pyproject.toml` under `[tool.ruff]`.
- Type checking is optional: mypy or Pyright (`ms-python.python` / Pylance).
- Commands: `ruff check .` and `ruff format .`.

## Java / Spring Boot

- Extension Pack for Java `vscjava.vscode-java-pack`.
- Build-time formatting: Spotless plugin (Maven/Gradle) or Checkstyle.
- Commands: `mvn spotless:apply` / `./gradlew spotlessApply` (only if the plugin is configured).

## C# / .NET

- C# Dev Kit `ms-dotnettools.csdevkit`.
- `dotnet format` driven by `.editorconfig` (put C# style rules there).
- Command: `dotnet format`.

## Flutter / Dart

- Dart `Dart-Code.dart-code` and Flutter `Dart-Code.flutter`.
- Built-in `dart format .`; lints via `analysis_options.yaml` and `flutter analyze`.

## Go

- Go extension `golang.go`. Formatting is built in and non-negotiable: `gofmt -l .` (list unformatted files) and `gofmt -w .` (rewrite).
- `go vet ./...` for built-in checks; optional `golangci-lint run` with `.golangci.yml` (check the installed version's config format).
- Tabs are the Go convention; do not set `indent_style = space` for `*.go` in `.editorconfig`.

## Rust

- rust-analyzer `rust-lang.rust-analyzer`.
- `cargo fmt` (config in `rustfmt.toml`; `cargo fmt --check` for CI) and `cargo clippy` (strict CI form: `cargo clippy --all-targets -- -D warnings`).

## Android (Kotlin)

- Android Studio / IntelliJ IDEA is the normal editor; no VS Code extension is required.
- ktlint and/or detekt through their Gradle plugins (for example `./gradlew ktlintCheck`, `./gradlew detekt` only if the plugin is configured); Android Lint via `./gradlew lint`. Check the project's plugin and Gradle versions before adding config files.

## iOS (Swift)

- Xcode is the normal editor; VS Code users can use the Swift extension `swiftlang.swift-vscode`.
- SwiftLint (`swiftlint`, config `.swiftlint.yml`) and/or swift-format (config `.swift-format`); check the installed version for the exact command (`swift format` ships with newer toolchains, otherwise install `swift-format`).

## Example `.vscode/extensions.json` (TS project, Option A)

```json
{
  "recommendations": [
    "EditorConfig.EditorConfig",
    "esbenp.prettier-vscode",
    "dbaeumer.vscode-eslint"
  ]
}
```

## When the user says "no third-party packages"

Do not recommend npm or pip tools (Prettier, ESLint, Ruff, ...). Use the built-ins instead and record `no formatter configured` as the evidence:
- JavaScript: `node --check <file>` for each source file, and tests with `node --test`.
- Python: `python -m compileall <dir>` and `python -W error -m unittest discover -s tests` (warnings as errors).
Still offer `.editorconfig` (it needs no package).

## Not on VS Code?

The same tools work elsewhere: `.editorconfig` is supported by JetBrains/Neovim/etc.; Prettier, ESLint, Biome, Ruff and `dart format` run from the CLI in any editor or CI. Mention the CLI command alongside the extension ID.

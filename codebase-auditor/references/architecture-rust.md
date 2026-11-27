## Rust (services / CLIs / libraries)
- Modules or workspace crates follow the declared style; domain types do not import the web or DB crate; `main` is thin and the logic lives in a library crate or module (testable).
- Errors are `Result`; library crates return typed errors; handlers map errors to responses in one place. `unwrap`/`expect`/indexing/slicing on user input or I/O is a finding; in tests or provably-infallible spots it is not.
- Every `unsafe` block has a `// SAFETY:` comment and is as small as possible; flag `unsafe` without justification.
- Async code: no blocking calls (sync I/O, heavy CPU, `std::thread::sleep`) on the executor; no `std::sync::Mutex` guard held across `.await`.
- `Cargo.lock` committed for binaries; `cargo clippy` and `cargo fmt --check` configured in CI.

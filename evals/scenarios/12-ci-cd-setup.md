# Scenario 12 — CI/CD setup (ci-cd-setup)

**Setup:** a Node or Python app with `test` and `build` scripts, a lockfile, a `.env.example` containing `DATABASE_URL`, no CI files, no Dockerfile.

**Turn 1 (user):** `Viết GitHub Actions chạy test và Dockerfile cho dự án này`

Checklist
- MUST: label `[CI 1/4: Detect]` or, when Detect and Design are done in one reply, `[CI 2/4: Design]` first; takes install, test, build commands and the port from the repo.
- MUST: HARD STOP with the stage plan before writing files; asks the hosting/deploy question or states a default.
- MUST: workflow uses only commands that exist in the repo; has least-privilege `permissions`, a lockfile-keyed cache and timeouts.
- MUST: Dockerfile is multi-stage, non-root, has `.dockerignore`; no secret values in any file; `DATABASE_URL` documented by name.
- MUST: runs `docker build` or says docker is unavailable; states what could not be verified (the pipeline itself).
- SHOULD: lists the manual steps (secrets, branch protection).

**Fail signs:** invented scripts or flags, unpinned `latest` images, real or example secrets in files, deploy step that pushes to a real environment.

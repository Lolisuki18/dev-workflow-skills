---
name: ci-cd-setup
description: "Sets up build, test and deploy automation for a project by reading its real stack first: writes a CI pipeline (GitHub Actions by default), a Dockerfile and compose file, environment and secrets handling, and a deploy and rollback guide, then checks them locally where possible. Use when the user says 'set up CI', 'write a GitHub Actions workflow', 'dockerize this app', 'add a Dockerfile', 'deploy this project', 'CI/CD pipeline', 'cache dependencies in CI', 'tạo pipeline CI/CD', 'viết Dockerfile', 'đóng gói docker cho dự án', 'cấu hình deploy', 'tự động chạy test khi push'. Do NOT use for fixing one failing CI job on a pull request (use ci-failure-triager from pull-request-skills), writing the project README (use readme-writer), changing application code (use dev-lifecycle), or database changes (use migration-writer)."
---

# CI/CD Setup

Automate build, test and deploy from what the repo actually uses. Never from a generic template pasted blindly.

## Anchor rule

Begin EVERY response with a step label: `[CI 1/4: Detect]` · `[CI 2/4: Design]` · `[CI 3/4: Write]` · `[CI 4/4: Verify & hand over]`.

## Ground rules

- Reply in the user's language; keep identifiers in English.
- Commands in the pipeline must exist in the repo (`package.json` scripts, `Makefile`, build files). Never invent a script, flag, image tag or action version: check the repo and the official docs, and cite what you used.
- **Secrets:** never write a real secret, token or password into any file. Use the CI provider's secret store and document the names. Add `.env` to ignore files and provide `.env.example`.
- Never trigger a real deploy, push an image or create cloud resources. Writing files and local checks only, unless the user explicitly asks for more.
- Pin versions of actions and base images; prefer the minimal image that works.

## Step 1 — Detect

1. Read the stack: language and version, package manager and lockfile, build tool, test command, lint and type-check commands, ports, required services (DB, cache), env variables used in code.
2. Find what exists already: `.github/workflows`, `Dockerfile`, `docker-compose*`, `Makefile`, deploy scripts. Extend, do not overwrite without asking.
3. Ask only what the repo cannot tell: hosting target, branching model, environments, who may deploy. Offer defaults (GitHub Actions, build and test on every PR, deploy manually from `main`).

## Step 2 — Design

Present a short plan: stages (install → lint → type-check → test → build → package → deploy), triggers, caches, matrix (versions or OS only if the project supports them), environments and approvals, secret names needed. Keep the first version small: a green build and test on every PR beats an elaborate pipeline.

### HARD STOP
Wait for approval before writing files. Hosting and deploy choices are the user's.

## Step 3 — Write

Load `references/pipeline-templates.md` for structure and adapt it to the detected commands.

- Workflow file(s) with least-privilege `permissions`, dependency cache keyed by the lockfile, and timeouts.
- `Dockerfile`: multi-stage, non-root user, `.dockerignore`, no secrets in layers, healthcheck when the app has an endpoint.
- `docker-compose.yml` for local development when services are needed.
- `docs/deploy.md` (or a section in the README): how to release, required secrets by name, how to roll back.

## Step 4 — Verify & hand over

1. Run what can run locally: lint the YAML, build the image (`docker build`), run the container's health or test command, run the test command the pipeline uses. Report real results; say what could not be run (the pipeline itself only runs on the provider).
2. List the manual steps the user must do: add secrets, enable branch protection, set up environments.
3. Report:

```
Files added/changed: ...
Pipeline stages: ...
Verified locally: <commands + results> | Not verified: <what>
User must do: <secrets, settings>
Risks / assumptions: ...
```

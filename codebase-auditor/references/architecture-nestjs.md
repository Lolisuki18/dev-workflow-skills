## NestJS (TypeScript)
- One module per feature (controller, service, dto, entity/schema); modules export only what others need; no circular module imports (`forwardRef` smell).
- Controllers thin; logic in providers/services; repositories or ORM calls not in controllers.
- Global `ValidationPipe` configured deliberately: `whitelist: true` only strips undecorated properties silently; add `forbidNonWhitelisted: true` to reject requests with unknown fields; `transform: true` is needed for payloads to become DTO instances. Whitelisting only affects properties that carry at least one class-validator decorator, so a DTO field with no decorator is dropped (or flagged) — check every body/query/param DTO field is decorated.
- Auth via guards on every protected route; ownership checks in the service; no business authorization only in the frontend.
- Exceptions mapped through filters/`HttpException`; config via `ConfigModule` validated at boot; no `process.env` scattered.

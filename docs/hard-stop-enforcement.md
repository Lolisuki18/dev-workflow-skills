# Enforcing the Hard Stops

Skills are instructions; a long context or a weaker model can ignore them. Three layers, from cheapest to strongest. Layers 1–2 are built in; layer 3 is optional and Claude Code only.

## Layer 1 — Anchors (built in)
- `[Phase X/5]` label on every full-mode reply, `[Bug X/5]` in bug-investigator.
- Each hard stop is written as a separate `HARD STOP` heading in the SKILL.md.

## Layer 2 — Artifact gate (built in)
The approval is stored in the plan file, not in the agent's memory:
- `feature-plan-writer` creates every plan with `Status: Draft`.
- After the user says "ok / code đi", the agent runs `init-plan.py --approve` (Status: Approved).
- Before writing code, `dev-lifecycle` runs `init-plan.py --require-approved`; exit code 3 means STOP.
- Anyone (or any later session) can check the state with `init-plan.py --status`.

## Layer 3 — Hook (optional, Claude Code)
[`scripts/plan-gate.py`](../scripts/plan-gate.py) is a PreToolUse hook: while the latest plan is `Status: Draft`, Write/Edit on anything outside `plan/` and `.gitignore` is refused (exit code 2), and the agent is told to get approval first. It fails open on any error, so it cannot break a session.

Add to `.claude/settings.json` of a project (or `~/.claude/settings.json` for all projects). Adjust the path to where you cloned this repo, and use `python3`/`py` if `python` is not on PATH:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          { "type": "command", "command": "python /path/to/dev-workflow-skills/scripts/plan-gate.py" }
        ]
      }
    ]
  }
}
```

Behavior to know:
- It only acts in projects that have a `plan/` folder whose latest plan is Draft. Projects without `plan/` are unaffected.
- Light-mode edits are blocked too while a Draft plan exists. Approve the plan, mark it Done, or delete the draft.
- Test it: create a Draft plan with `init-plan.py "x"`, ask the agent to edit a source file, and confirm it is refused; run `init-plan.py --approve` and confirm it passes.
- Other agents (Cursor, Gemini CLI, Codex) have their own hook mechanisms; layers 1–2 still apply.

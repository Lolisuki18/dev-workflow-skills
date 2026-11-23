#!/usr/bin/env python3
"""OPTIONAL Claude Code PreToolUse hook: block source edits while the latest plan is still Draft.

This turns the dev-lifecycle Phase 2 hard stop from a written rule into a mechanical one:
as long as plan/ exists and its latest plan says `Status: Draft`, Write/Edit calls on files
outside plan/ and .gitignore are refused with a message telling the agent to get approval.

Reads the hook JSON from stdin. Exit 0 = allow, exit 2 = block (stderr is shown to the agent).
Fails OPEN on any parse problem so it never bricks a session.
Opt-in: see docs/hard-stop-enforcement.md.
"""
import json
import re
import sys
from pathlib import Path

STATUS_RE = re.compile(r"^Status:\s*(.+?)\s*$", re.M)
ALLOW_TOP = {"plan", ".gitignore"}


def find_root(start: Path) -> Path:
    for p in [start, *start.parents]:
        if (p / ".git").exists() or (p / "plan").is_dir():
            return p
    return start


def main() -> int:
    try:
        data = json.load(sys.stdin)
        tool_input = data.get("tool_input") or {}
        file_path = tool_input.get("file_path") or tool_input.get("path")
        cwd = Path(data.get("cwd") or ".").resolve()
        if not file_path:
            return 0
        target = Path(file_path)
        if not target.is_absolute():
            target = (cwd / target).resolve()
        root = find_root(cwd)
        plan_dir = root / "plan"
        plans = sorted(plan_dir.glob("*.md")) if plan_dir.is_dir() else []
        if not plans:
            return 0
        try:
            rel = target.relative_to(root)
        except ValueError:
            return 0  # outside the project
        if rel.parts and rel.parts[0] in ALLOW_TOP:
            return 0
        m = STATUS_RE.search(plans[-1].read_text(encoding="utf-8"))
        status = m.group(1) if m else "unknown"
        if status == "Draft":
            print(
                f"BLOCKED by plan-gate: {plans[-1].relative_to(root).as_posix()} is still 'Status: Draft'. "
                "Present the plan and wait for the user's approval, then run init-plan.py --approve. "
                "(Small edits: ask the user to approve or disable the hook.)",
                file=sys.stderr,
            )
            return 2
        return 0
    except Exception:
        return 0


if __name__ == "__main__":
    sys.exit(main())

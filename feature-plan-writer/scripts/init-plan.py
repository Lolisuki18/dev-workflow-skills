#!/usr/bin/env python3
"""Create the next plan file in plan/ and make sure plan/ is git-ignored.

Usage:
  python init-plan.py "Feature name"            # create plan file (+ .gitignore entry)
  python init-plan.py "Feature name" --date     # force YYYY-MM-DD-name.md naming
  python init-plan.py --check                   # read-only: list plans, next number, .gitignore state
  python init-plan.py "Name" --root <dir>       # repo root (default: nearest .git upward, else cwd)
  python init-plan.py --status                  # print latest plan's Status
  python init-plan.py --approve                 # set latest plan Status: Approved (after the user said ok)
  python init-plan.py --set-status "In progress"  # Draft | Approved | In progress | Done
  python init-plan.py --share                   # team mode: stop ignoring plan/ (plans get committed)
  python init-plan.py --gate off|on             # create/remove plan/.no-gate for the optional hook
  (gitignore= result: created | added | already | skipped-tracked | removed | not-present;
   --check only reports: would-create | would-add | already | skipped-tracked)
  python init-plan.py --require-approved        # exit 3 unless latest plan is Approved / In progress
  (--plan NAME.md selects a plan other than the latest)

Stdlib only. Never overwrites an existing plan. Prints key=value lines:
  plan_file=..., scheme=..., gitignore=added|already|created, existing_plans=N
  --check adds: plan_dir=exists|missing, next_plan=<number or date>; it changes nothing on disk
Exit codes: 0 ok, 1 error.
"""
import argparse
import re
import subprocess
import sys
import unicodedata
from datetime import date
from pathlib import Path

NUM_RE = re.compile(r"^(\d+)-.+\.md$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-.+\.md$")
TEMPLATE = Path(__file__).resolve().parent.parent / "references" / "plan-template.md"


def find_root(start: Path) -> Path:
    for p in [start, *start.parents]:
        if (p / ".git").exists():
            return p
    return start


def slugify(text: str) -> str:
    text = text.replace("đ", "d").replace("Đ", "D")
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return slug or "feature"


def plan_key(p: Path) -> tuple[int, int, str]:
    """Sort key: other names, then date-named, then numbered (by integer). The last item is the latest plan.
    Keep identical to plan_key in scripts/plan-gate.py (tests check both)."""
    m = NUM_RE.match(p.name)
    if m and not DATE_RE.match(p.name):
        return (2, int(m.group(1)), p.name)
    if DATE_RE.match(p.name):
        return (1, 0, p.name)
    return (0, 0, p.name)


STATUS_RE = re.compile(r"^Status:\s*(.+?)\s*$", re.M)


def get_status(path: Path) -> str:
    m = STATUS_RE.search(path.read_text(encoding="utf-8"))
    return m.group(1) if m else "unknown"


def set_status(path: Path, value: str) -> None:
    text = path.read_text(encoding="utf-8")
    if STATUS_RE.search(text):
        text = STATUS_RE.sub(f"Status: {value}", text, count=1)
    else:
        text = f"Status: {value}\n" + text
    path.write_text(text, encoding="utf-8")


IGNORE_LINES = ("plan/", "/plan/", "plan", "/plan")


def plan_is_tracked(root: Path) -> bool:
    """True if git already tracks files under plan/ (the team shares plans on purpose)."""
    try:
        out = subprocess.run(
            ["git", "-C", str(root), "ls-files", "--", "plan"],
            capture_output=True, text=True, timeout=10,
        )
        return out.returncode == 0 and bool(out.stdout.strip())
    except Exception:
        return False


def remove_gitignore_entry(root: Path) -> str:
    """--share: drop the plan/ line so plans can be committed."""
    gi = root / ".gitignore"
    if not gi.exists():
        return "not-present"
    lines = gi.read_text(encoding="utf-8").splitlines()
    kept = [ln for ln in lines if ln.strip() not in IGNORE_LINES]
    if len(kept) == len(lines):
        return "not-present"
    gi.write_text("\n".join(kept) + ("\n" if kept else ""), encoding="utf-8")
    return "removed"


def ensure_gitignore(root: Path) -> str:
    if plan_is_tracked(root):
        return "skipped-tracked"
    gi = root / ".gitignore"
    if not gi.exists():
        gi.write_text("plan/\n", encoding="utf-8")
        return "created"
    content = gi.read_text(encoding="utf-8")
    lines = [ln.strip() for ln in content.splitlines()]
    if any(ln in IGNORE_LINES for ln in lines):
        return "already"
    sep = "" if content == "" or content.endswith("\n") else "\n"
    gi.write_text(content + sep + "plan/\n", encoding="utf-8")
    return "added"


def gitignore_state(root: Path) -> str:
    """Read-only twin of ensure_gitignore for --check: what the plan-creation call would do."""
    if plan_is_tracked(root):
        return "skipped-tracked"
    gi = root / ".gitignore"
    if not gi.exists():
        return "would-create"
    if any(ln.strip() in IGNORE_LINES for ln in gi.read_text(encoding="utf-8").splitlines()):
        return "already"
    return "would-add"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("title", nargs="?", help="feature name")
    ap.add_argument("--date", action="store_true", help="use date-based naming")
    ap.add_argument("--check", action="store_true", help="no new file")
    ap.add_argument("--root", help="repo root")
    ap.add_argument("--status", action="store_true", help="print status of latest plan")
    ap.add_argument("--approve", action="store_true", help="set latest plan Status to Approved")
    ap.add_argument("--require-approved", action="store_true",
                    help="exit 3 unless the latest plan is Approved / In progress")
    ap.add_argument("--set-status", choices=["Draft", "Approved", "In progress", "Done"],
                    help="set latest plan Status to this value")
    ap.add_argument("--plan", help="plan file name to use instead of the latest")
    ap.add_argument("--share", action="store_true",
                    help="team mode: remove the plan/ line from .gitignore so plans can be committed")
    ap.add_argument("--gate", choices=["on", "off"],
                    help="off: create plan/.no-gate so the optional plan-gate hook stops blocking; on: remove it")
    args = ap.parse_args()

    root = Path(args.root).resolve() if args.root else find_root(Path.cwd())
    plan_dir = root / "plan"

    if args.gate:
        marker = plan_dir / ".no-gate"
        if args.gate == "off":
            plan_dir.mkdir(exist_ok=True)
            marker.write_text("plan-gate disabled for this project\n", encoding="utf-8")
        elif marker.exists():
            marker.unlink()
        print(f"gate={args.gate}")
        return 0

    if args.status or args.approve or args.require_approved or args.set_status:
        plans = sorted(plan_dir.glob("*.md"), key=plan_key) if plan_dir.is_dir() else []
        target = (plan_dir / args.plan) if args.plan else (plans[-1] if plans else None)
        if target is None or not target.exists():
            print("plan_status=none")
            return 3 if args.require_approved else 1
        if args.approve:
            set_status(target, "Approved")
        elif args.set_status:
            set_status(target, args.set_status)
        st = get_status(target)
        print(f"plan_file={target.relative_to(root).as_posix()}")
        print(f"plan_status={st}")
        if args.require_approved and st not in ("Approved", "In progress"):
            return 3
        return 0

    if not args.title and not args.check:
        ap.error("title required unless --check")

    names = sorted(p.name for p in plan_dir.glob("*.md")) if plan_dir.is_dir() else []
    numbered = [n for n in names if NUM_RE.match(n) and not DATE_RE.match(n)]
    dated = [n for n in names if DATE_RE.match(n)]
    use_date = args.date or (dated and len(dated) > len(numbered))
    scheme = "date" if use_date else "number"

    print(f"root={root}")
    print(f"existing_plans={len(names)}")
    for n in names:
        print(f"existing={n}")

    today = date.today().isoformat()
    if use_date:
        number = today
    else:
        nums = [int(NUM_RE.match(n).group(1)) for n in numbered]
        number = f"{(max(nums) + 1 if nums else 1):03d}"

    if args.check and not args.share:
        # Read-only: report only, so a brownfield repo is untouched before the plan is approved.
        print(f"plan_dir={'exists' if plan_dir.is_dir() else 'missing'}")
        print(f"next_plan={number}")
        print(f"gitignore={gitignore_state(root)}")
        return 0

    status = remove_gitignore_entry(root) if args.share else ensure_gitignore(root)
    print(f"gitignore={status}")

    if args.check:
        return 0

    plan_dir.mkdir(exist_ok=True)

    slug = slugify(args.title)
    fname = f"{today}-{slug}.md" if use_date else f"{number}-{slug}.md"

    target = plan_dir / fname
    if target.exists():
        print(f"error: {target} already exists", file=sys.stderr)
        return 1
    if not TEMPLATE.exists():
        print(f"error: template not found: {TEMPLATE}", file=sys.stderr)
        return 1

    body = (
        TEMPLATE.read_text(encoding="utf-8")
        .replace("{number}", number)
        .replace("{title}", args.title)
        .replace("{date}", today)
    )
    target.write_text(body, encoding="utf-8")
    print(f"scheme={scheme}")
    print(f"plan_file={target.relative_to(root).as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

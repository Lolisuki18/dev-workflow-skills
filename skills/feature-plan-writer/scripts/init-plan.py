#!/usr/bin/env python3
"""Create the next plan file in plan/ and make sure plan/ is git-ignored.

Usage:
  python init-plan.py "Feature name"            # create plan file (+ fix .gitignore)
  python init-plan.py "Feature name" --date     # force YYYY-MM-DD-name.md naming
  python init-plan.py --check                   # only list plans + fix .gitignore
  python init-plan.py "Name" --root <dir>       # repo root (default: nearest .git upward, else cwd)

Stdlib only. Never overwrites an existing plan. Prints key=value lines:
  plan_file=..., scheme=..., gitignore=added|already|created, existing_plans=N
Exit codes: 0 ok, 1 error.
"""
import argparse
import re
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


def ensure_gitignore(root: Path) -> str:
    gi = root / ".gitignore"
    if not gi.exists():
        gi.write_text("plan/\n", encoding="utf-8")
        return "created"
    content = gi.read_text(encoding="utf-8")
    lines = [ln.strip() for ln in content.splitlines()]
    if any(ln in ("plan/", "/plan/", "plan", "/plan") for ln in lines):
        return "already"
    sep = "" if content == "" or content.endswith("\n") else "\n"
    gi.write_text(content + sep + "plan/\n", encoding="utf-8")
    return "added"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("title", nargs="?", help="feature name")
    ap.add_argument("--date", action="store_true", help="use date-based naming")
    ap.add_argument("--check", action="store_true", help="no new file")
    ap.add_argument("--root", help="repo root")
    args = ap.parse_args()

    if not args.title and not args.check:
        ap.error("title required unless --check")

    root = Path(args.root).resolve() if args.root else find_root(Path.cwd())
    plan_dir = root / "plan"
    plan_dir.mkdir(exist_ok=True)

    names = sorted(p.name for p in plan_dir.glob("*.md"))
    numbered = [n for n in names if NUM_RE.match(n) and not DATE_RE.match(n)]
    dated = [n for n in names if DATE_RE.match(n)]
    use_date = args.date or (dated and len(dated) > len(numbered))
    scheme = "date" if use_date else "number"

    print(f"root={root}")
    print(f"existing_plans={len(names)}")
    for n in names:
        print(f"existing={n}")

    status = ensure_gitignore(root)
    print(f"gitignore={status}")

    if args.check:
        return 0

    slug = slugify(args.title)
    today = date.today().isoformat()
    if use_date:
        fname = f"{today}-{slug}.md"
        number = today
    else:
        nums = [int(NUM_RE.match(n).group(1)) for n in numbered]
        number = f"{(max(nums) + 1 if nums else 1):03d}"
        fname = f"{number}-{slug}.md"

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

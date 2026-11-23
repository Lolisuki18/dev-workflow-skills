#!/usr/bin/env python3
"""Link (or copy) every skill folder of this repo into an agent's skills directory.

Usage:
  python scripts/install.py                       # link into ~/.claude/skills
  python scripts/install.py --target ~/.cursor/skills
  python scripts/install.py --copy                # copy instead of link
  python scripts/install.py --dry-run             # show what would happen
  python scripts/install.py --uninstall           # remove links/copies made from this repo

A skill is any top-level folder here that contains SKILL.md. Existing entries are never
overwritten: they are reported as `exists` (or `replaced` only with --force, links only).
Windows: uses directory junctions (no admin rights). POSIX: symlinks.
Stdlib only.
"""
import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def skills():
    return sorted(p for p in REPO.iterdir() if p.is_dir() and (p / "SKILL.md").exists())


def is_link(p: Path) -> bool:
    if p.is_symlink():
        return True
    if os.name == "nt":
        try:
            # lstat does not follow the junction, so the reparse-point flag is visible
            return bool(os.lstat(p).st_file_attributes & 0x400)
        except (OSError, AttributeError):
            return False
    return False


def link_target(p: Path):
    try:
        return Path(os.path.realpath(p))
    except OSError:
        return None


def make_link(src: Path, dst: Path) -> None:
    if os.name == "nt":
        r = subprocess.run(["cmd", "/c", "mklink", "/J", str(dst), str(src)],
                           capture_output=True, text=True)
        if r.returncode != 0:
            raise OSError(r.stderr.strip() or r.stdout.strip())
    else:
        os.symlink(src, dst, target_is_directory=True)


def remove_link(p: Path) -> None:
    if os.name == "nt" and not p.is_symlink():
        subprocess.run(["cmd", "/c", "rmdir", str(p)], capture_output=True)  # removes junction only
    else:
        p.unlink()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--target", default=str(Path.home() / ".claude" / "skills"))
    ap.add_argument("--copy", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--uninstall", action="store_true")
    ap.add_argument("--force", action="store_true", help="replace an existing LINK that points elsewhere")
    args = ap.parse_args()

    target = Path(args.target).expanduser()
    names = skills()
    if not names:
        print("error: no skills found", file=sys.stderr)
        return 1
    if not args.dry_run and not args.uninstall:
        target.mkdir(parents=True, exist_ok=True)

    rc = 0
    for src in names:
        dst = target / src.name
        try:
            if args.uninstall:
                if not dst.exists() and not is_link(dst):
                    print(f"absent    {src.name}")
                elif is_link(dst) and link_target(dst) == src.resolve():
                    if not args.dry_run:
                        remove_link(dst)
                    print(f"removed   {src.name}")
                else:
                    print(f"skipped   {src.name} (not a link to this repo; remove it yourself)")
                continue

            if dst.exists() or is_link(dst):
                if is_link(dst) and link_target(dst) == src.resolve():
                    print(f"ok        {src.name} (already linked)")
                elif is_link(dst) and args.force:
                    if not args.dry_run:
                        remove_link(dst)
                        make_link(src, dst)
                    print(f"replaced  {src.name}")
                else:
                    print(f"exists    {src.name} (left untouched)")
                continue

            if args.dry_run:
                print(f"would {'copy' if args.copy else 'link'} {src.name}")
            elif args.copy:
                shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
                print(f"copied    {src.name}")
            else:
                make_link(src, dst)
                print(f"linked    {src.name}")
        except OSError as e:
            rc = 1
            print(f"error     {src.name}: {e}", file=sys.stderr)
    return rc


if __name__ == "__main__":
    sys.exit(main())

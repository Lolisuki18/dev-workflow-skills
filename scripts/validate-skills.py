#!/usr/bin/env python3
"""Validate every skill in skills/ against the repo rules.

Usage: python scripts/validate-skills.py [--skills-dir <repo root>]   (skills are the root-level folders)
Exit code 1 if any ERROR is found (warnings do not fail). Stdlib only.

Checks per skills/<name>/SKILL.md:
  ERROR  frontmatter present with `name` and `description`
  ERROR  name is kebab-case and equals the folder name
  ERROR  description <= 1024 chars, contains 'Do NOT use'
  ERROR  SKILL.md <= 250 lines
  ERROR  every `references/...` or `scripts/...` path mentioned exists
  WARN   description does not start with a third-person verb (heuristic: first word ends in 's')
  WARN   description has no Vietnamese trigger (no diacritics found)
  WARN   a file in references/ or scripts/ is never mentioned in SKILL.md
  WARN   a references/ file links to another references/ file (depth > 1)
"""
import argparse
import re
import sys
from pathlib import Path

MAX_LINES = 250
MAX_DESC = 1024
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
PATH_RE = re.compile(r"`((?:references|scripts)/[A-Za-z0-9_./-]+)`")
VI_RE = re.compile(r"[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]", re.I)


def parse_frontmatter(text: str):
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    fm = {}
    for line in text[3:end].splitlines():
        m = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if m:
            val = m.group(2).strip()
            if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
                val = val[1:-1]
            fm[m.group(1)] = val
    return fm


def check_skill(d: Path):
    errors, warns = [], []
    skill = d / "SKILL.md"
    if not skill.exists():
        return [f"{d.name}: SKILL.md missing"], warns
    text = skill.read_text(encoding="utf-8")
    lines = text.count("\n") + (0 if text.endswith("\n") else 1)

    fm = parse_frontmatter(text)
    if fm is None or "name" not in fm or "description" not in fm:
        return [f"{d.name}: frontmatter missing name/description"], warns

    name, desc = fm["name"], fm["description"]
    if not KEBAB.match(name):
        errors.append(f"{d.name}: name '{name}' is not kebab-case")
    if name != d.name:
        errors.append(f"{d.name}: name '{name}' != folder name")
    if len(desc) > MAX_DESC:
        errors.append(f"{d.name}: description {len(desc)} chars > {MAX_DESC}")
    if "Do NOT use" not in desc:
        errors.append(f"{d.name}: description lacks 'Do NOT use'")
    first = desc.split(" ", 1)[0] if desc else ""
    if not first.endswith("s"):
        warns.append(f"{d.name}: description may not be third person (starts '{first}')")
    if not VI_RE.search(desc):
        warns.append(f"{d.name}: description has no Vietnamese trigger keywords")
    if lines > MAX_LINES:
        errors.append(f"{d.name}: SKILL.md has {lines} lines > {MAX_LINES}")

    mentioned = set(PATH_RE.findall(text))
    for rel in sorted(mentioned):
        if not (d / rel).exists():
            errors.append(f"{d.name}: referenced path not found: {rel}")

    for sub in ("references", "scripts"):
        folder = d / sub
        if folder.is_dir():
            for f in sorted(p for p in folder.rglob("*") if p.is_file()):
                rel = f.relative_to(d).as_posix()
                if rel not in mentioned:
                    warns.append(f"{d.name}: {rel} never mentioned in SKILL.md")
                if sub == "references" and f.suffix == ".md":
                    inner = f.read_text(encoding="utf-8")
                    if re.search(r"`references/[A-Za-z0-9_./-]+`", inner):
                        warns.append(f"{d.name}: {rel} links to another references file (depth > 1)")
    scripts_dir = d / "scripts"
    if scripts_dir.is_dir():
        for py in sorted(scripts_dir.glob("*.py")):
            try:
                compile(py.read_text(encoding="utf-8"), str(py), "exec")
            except SyntaxError as e:
                errors.append(f"{d.name}: {py.name} has a syntax error: {e}")
    return errors, warns


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skills-dir", default=str(Path(__file__).resolve().parent.parent))
    args = ap.parse_args()
    root = Path(args.skills_dir)
    # a skill is any direct subfolder holding SKILL.md (or a subfolder not starting with '.' / named scripts when root is a skills-only dir)
    dirs = (
        sorted(p for p in root.iterdir() if p.is_dir() and not p.name.startswith(".") and p.name not in ("scripts", "evals", "hooks", "docs", "tests"))
        if root.is_dir()
        else []
    )
    if not dirs:
        print(f"ERROR no skills found in {root}")
        return 1

    total_err = 0
    for d in dirs:
        errs, warns = check_skill(d)
        status = "FAIL" if errs else "ok"
        print(f"[{status}] {d.name}")
        for e in errs:
            print(f"  ERROR {e}")
        for w in warns:
            print(f"  WARN  {w}")
        total_err += len(errs)
    print(f"\n{len(dirs)} skills checked, {total_err} error(s)")
    return 1 if total_err else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Automated tests for the helper scripts (stdlib unittest, no installs).

Run:  python -m unittest discover -s tests -v      (from the repo root)

Covers feature-plan-writer/scripts/init-plan.py and scripts/plan-gate.py.
Needs `git` on PATH (used to create throwaway repos in temp dirs).
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
INIT = REPO / "feature-plan-writer" / "scripts" / "init-plan.py"
GATE = REPO / "scripts" / "plan-gate.py"


def run(script, args, cwd, stdin=None, env=None):
    e = {**os.environ, **(env or {})}
    return subprocess.run(
        [sys.executable, str(script), *args],
        cwd=str(cwd), input=stdin, capture_output=True, text=True, env=e,
    )


def kv(stdout):
    out = {}
    for line in stdout.splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            out.setdefault(k, v)
    return out


class TempRepo(unittest.TestCase):
    def setUp(self):
        self._td = tempfile.TemporaryDirectory()
        self.root = Path(self._td.name).resolve()
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)

    def tearDown(self):
        self._td.cleanup()

    def init(self, *args, **kw):
        return run(INIT, list(args), self.root, **kw)

    def gitignore(self):
        p = self.root / ".gitignore"
        return p.read_text(encoding="utf-8") if p.exists() else None


class InitPlanTests(TempRepo):
    def test_numbering_is_sequential_and_slug_is_ascii(self):
        r1 = self.init("Đăng nhập người dùng")
        r2 = self.init("Học từ vựng")
        self.assertEqual(kv(r1.stdout)["plan_file"], "plan/001-dang-nhap-nguoi-dung.md")
        self.assertEqual(kv(r2.stdout)["plan_file"], "plan/002-hoc-tu-vung.md")

    def test_plan_file_has_header_and_draft_status(self):
        self.init("Demo")
        text = (self.root / "plan" / "001-demo.md").read_text(encoding="utf-8")
        self.assertIn("# 001 — Demo", text)
        self.assertIn("Status: Draft", text)
        self.assertIn("## 10. Resume point", text)

    def test_gitignore_created_added_and_not_duplicated(self):
        self.assertEqual(kv(self.init("A").stdout)["gitignore"], "created")
        self.assertEqual(kv(self.init("B").stdout)["gitignore"], "already")
        self.assertEqual(self.gitignore().count("plan/"), 1)

    def test_gitignore_keeps_existing_entries(self):
        (self.root / ".gitignore").write_text("node_modules", encoding="utf-8")  # no trailing newline
        self.assertEqual(kv(self.init("A").stdout)["gitignore"], "added")
        lines = self.gitignore().splitlines()
        self.assertEqual(lines, ["node_modules", "plan/"])

    def test_date_scheme_and_no_overwrite(self):
        r = self.init("Same", "--date")
        self.assertRegex(kv(r.stdout)["plan_file"], r"^plan/\d{4}-\d{2}-\d{2}-same\.md$")
        again = self.init("Same", "--date")
        self.assertEqual(again.returncode, 1)
        self.assertIn("already exists", again.stderr)

    def test_existing_date_plans_keep_date_scheme(self):
        self.init("First", "--date")
        r = self.init("Second")
        self.assertEqual(kv(r.stdout)["scheme"], "date")

    def test_status_approve_set_status_and_require_approved(self):
        self.assertEqual(self.init("--require-approved").returncode, 3)  # no plan at all
        self.init("Demo")
        self.assertEqual(kv(self.init("--status").stdout)["plan_status"], "Draft")
        self.assertEqual(self.init("--require-approved").returncode, 3)  # Draft blocks
        self.assertEqual(kv(self.init("--approve").stdout)["plan_status"], "Approved")
        self.assertEqual(self.init("--require-approved").returncode, 0)
        self.assertEqual(kv(self.init("--set-status", "In progress").stdout)["plan_status"], "In progress")
        self.assertEqual(self.init("--require-approved").returncode, 0)
        self.assertEqual(kv(self.init("--set-status", "Done").stdout)["plan_status"], "Done")
        self.assertEqual(self.init("--require-approved").returncode, 3)

    def test_set_status_rejects_unknown_value(self):
        self.init("Demo")
        self.assertNotEqual(self.init("--set-status", "Banana").returncode, 0)

    def test_status_targets_latest_plan(self):
        self.init("One")
        self.init("Two")
        self.init("--approve")
        one = (self.root / "plan" / "001-one.md").read_text(encoding="utf-8")
        two = (self.root / "plan" / "002-two.md").read_text(encoding="utf-8")
        self.assertIn("Status: Draft", one)
        self.assertIn("Status: Approved", two)

    def test_share_removes_ignore_line_and_keeps_others(self):
        (self.root / ".gitignore").write_text("node_modules\nplan/\n.env\n", encoding="utf-8")
        r = self.init("--check", "--share")
        self.assertEqual(kv(r.stdout)["gitignore"], "removed")
        self.assertEqual(self.gitignore().splitlines(), ["node_modules", ".env"])
        self.assertEqual(kv(self.init("--check", "--share").stdout)["gitignore"], "not-present")

    def test_tracked_plan_dir_is_left_alone(self):
        self.init("Demo")
        subprocess.run(["git", "add", "-f", "plan/001-demo.md"], cwd=self.root, check=True)
        (self.root / ".gitignore").write_text("", encoding="utf-8")
        r = self.init("--check")
        self.assertEqual(kv(r.stdout)["gitignore"], "skipped-tracked")
        self.assertNotIn("plan/", self.gitignore())

    def test_gate_marker_toggle(self):
        self.init("--gate", "off")
        self.assertTrue((self.root / "plan" / ".no-gate").exists())
        self.init("--gate", "on")
        self.assertFalse((self.root / "plan" / ".no-gate").exists())


class PlanGateTests(TempRepo):
    def call(self, rel_path, env=None, raw=None):
        payload = raw if raw is not None else json.dumps({
            "tool_name": "Write",
            "tool_input": {"file_path": str(self.root / rel_path)},
            "cwd": str(self.root),
        })
        return run(GATE, [], self.root, stdin=payload, env=env)

    def test_no_plan_dir_allows(self):
        self.assertEqual(self.call("src/a.ts").returncode, 0)

    def test_draft_blocks_source_but_not_plan_or_gitignore(self):
        self.init("Demo")
        blocked = self.call("src/a.ts")
        self.assertEqual(blocked.returncode, 2)
        self.assertIn("Draft", blocked.stderr)
        self.assertEqual(self.call("plan/001-demo.md").returncode, 0)
        self.assertEqual(self.call(".gitignore").returncode, 0)

    def test_approved_and_in_progress_allow(self):
        self.init("Demo")
        self.init("--approve")
        self.assertEqual(self.call("src/a.ts").returncode, 0)
        self.init("--set-status", "In progress")
        self.assertEqual(self.call("src/a.ts").returncode, 0)

    def test_env_var_and_marker_bypass(self):
        self.init("Demo")
        self.assertEqual(self.call("src/a.ts", env={"PLAN_GATE": "off"}).returncode, 0)
        self.init("--gate", "off")
        self.assertEqual(self.call("src/a.ts").returncode, 0)
        self.init("--gate", "on")
        self.assertEqual(self.call("src/a.ts").returncode, 2)

    def test_fails_open_on_garbage_and_outside_project(self):
        self.init("Demo")
        self.assertEqual(self.call("src/a.ts", raw="not json").returncode, 0)
        outside = json.dumps({
            "tool_name": "Write",
            "tool_input": {"file_path": str(self.root.parent / "other" / "x.ts")},
            "cwd": str(self.root),
        })
        self.assertEqual(self.call("x", raw=outside).returncode, 0)

    def init(self, *args):
        return run(INIT, list(args), self.root)


VALIDATE = REPO / "scripts" / "validate-skills.py"


class ValidateTests(unittest.TestCase):
    def make_skill(self, root, review_line):
        d = Path(root) / "demo-skill"
        (d / "references").mkdir(parents=True)
        (d / "SKILL.md").write_text(
            '---\nname: demo-skill\ndescription: "Does demo things. Use when xin chào. '
            'Do NOT use for others."\n---\nSee `references/rules.md`.\n', encoding="utf-8")
        (d / "references" / "rules.md").write_text(f"# Rules\n{review_line}\n", encoding="utf-8")

    def validate(self, root):
        return run(VALIDATE, ["--skills-dir", str(root)], REPO)

    def test_overdue_review_warns_but_does_not_fail(self):
        with tempfile.TemporaryDirectory() as td:
            self.make_skill(td, "Next review: 2000-01-01")
            r = self.validate(td)
            self.assertEqual(r.returncode, 0, r.stdout)
            self.assertIn("review overdue", r.stdout)

    def test_future_review_is_quiet_and_bad_date_warns(self):
        with tempfile.TemporaryDirectory() as td:
            self.make_skill(td, "Next review: 2999-01-01")
            self.assertNotIn("overdue", self.validate(td).stdout)
        with tempfile.TemporaryDirectory() as td:
            self.make_skill(td, "Next review: soon")
            self.assertIn("invalid 'Next review:'", self.validate(td).stdout)

    def test_repo_architecture_rules_have_review_dates(self):
        text = (REPO / "codebase-auditor" / "references" / "architecture-rules.md").read_text(encoding="utf-8")
        self.assertRegex(text, r"(?m)^Last verified: \d{4}-\d{2}-\d{2}$")
        self.assertRegex(text, r"(?m)^Next review: \d{4}-\d{2}-\d{2}$")


INSTALL = REPO / "scripts" / "install.py"


class InstallTests(unittest.TestCase):
    def setUp(self):
        self._td = tempfile.TemporaryDirectory()
        self.target = Path(self._td.name) / "skills"

    def tearDown(self):
        self._td.cleanup()

    def install(self, *args):
        return run(INSTALL, ["--target", str(self.target), *args], REPO)

    def test_dry_run_changes_nothing(self):
        r = self.install("--dry-run")
        self.assertEqual(r.returncode, 0)
        self.assertIn("would link dev-lifecycle", r.stdout)
        self.assertFalse(self.target.exists())

    def test_copy_installs_all_skills_and_is_idempotent(self):
        r = self.install("--copy")
        self.assertEqual(r.returncode, 0, r.stderr)
        for name in ("dev-lifecycle", "feature-plan-writer", "test-case-writer",
                     "codebase-auditor", "bug-investigator"):
            self.assertTrue((self.target / name / "SKILL.md").exists(), name)
        self.assertFalse((self.target / "scripts").exists())  # helper folders are not skills
        again = self.install("--copy")
        self.assertIn("exists", again.stdout)  # never overwrites

    def test_link_then_uninstall(self):
        r = self.install()
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue((self.target / "dev-lifecycle" / "SKILL.md").exists())
        self.assertIn("already linked", self.install().stdout)
        u = self.install("--uninstall")
        self.assertIn("removed   dev-lifecycle", u.stdout)
        self.assertFalse((self.target / "dev-lifecycle").exists())
        self.assertTrue((REPO / "dev-lifecycle" / "SKILL.md").exists())  # source untouched

    def test_uninstall_leaves_foreign_copy_alone(self):
        self.install("--copy")
        u = self.install("--uninstall")
        self.assertIn("skipped", u.stdout)
        self.assertTrue((self.target / "dev-lifecycle" / "SKILL.md").exists())


if __name__ == "__main__":
    unittest.main()

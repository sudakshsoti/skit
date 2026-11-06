#!/usr/bin/env python3
"""Tests for scripts/lint.py: how skills start, and whether they work with no agents.

Each test copies the repo's skills, agents and README into a temp tree, breaks
one thing, and checks what lint reports. Run: python3 scripts/test-lint.py
"""
from __future__ import annotations

import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("lint", REPO / "scripts" / "lint.py")
lint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lint)


class LintTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        for part in ("skills", "agents"):
            shutil.copytree(REPO / part, self.tmp / part)
        shutil.copy(REPO / "README.md", self.tmp / "README.md")

    def problems(self):
        return lint.lint(self.tmp)

    def test_repo_as_shipped_is_clean(self):
        self.assertEqual(lint.lint(REPO), [])

    def test_ux_copy_and_handoff_start_automatically(self):
        for name in ("soti-ux-copy", "soti-handoff"):
            text = (REPO / "skills" / name / "SKILL.md").read_text()
            self.assertNotIn("disable-model-invocation", text, name)

    def test_lint_rejects_a_manual_only_ux_copy(self):
        f = self.tmp / "skills" / "soti-ux-copy" / "SKILL.md"
        f.write_text(f.read_text().replace("\n---\n", "\ndisable-model-invocation: true\n---\n", 1))
        self.assertTrue(any("soti-ux-copy" in p and "start automatically" in p for p in self.problems()))

    def test_lint_rejects_a_skill_that_reads_the_agents_folder(self):
        f = self.tmp / "skills" / "soti-vibe" / "SKILL.md"
        f.write_text(f.read_text() + "\nRead `../../agents/soti-critic.md`.\n")
        self.assertTrue(any("agents folder" in p for p in self.problems()))

    def test_vibe_ships_the_critic_rules_in_the_skill(self):
        self.assertTrue((REPO / "skills" / "soti-vibe" / "references" / "critic.md").is_file())

    def test_lint_rejects_critic_rules_that_drifted_from_the_agent(self):
        f = self.tmp / "skills" / "soti-vibe" / "references" / "critic.md"
        f.write_text(f.read_text() + "\nExtra rule.\n")
        self.assertTrue(any("critic rules differ" in p for p in self.problems()))


if __name__ == "__main__":
    unittest.main()

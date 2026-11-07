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
        shutil.copytree(REPO / ".claude-plugin", self.tmp / ".claude-plugin")

    def problems(self):
        return lint.lint(self.tmp)

    def test_repo_as_shipped_is_clean(self):
        self.assertEqual(lint.lint(REPO), [])

    def test_ux_copy_and_handoff_start_automatically(self):
        for name in ("skit-ux-copy", "skit-handoff"):
            text = (REPO / "skills" / name / "SKILL.md").read_text()
            self.assertNotIn("disable-model-invocation", text, name)

    def test_lint_rejects_a_manual_only_ux_copy(self):
        f = self.tmp / "skills" / "skit-ux-copy" / "SKILL.md"
        f.write_text(f.read_text().replace("\n---\n", "\ndisable-model-invocation: true\n---\n", 1))
        self.assertTrue(any("skit-ux-copy" in p and "start automatically" in p for p in self.problems()))

    def test_lint_rejects_a_skill_that_reads_the_agents_folder(self):
        f = self.tmp / "skills" / "skit-vibe" / "SKILL.md"
        f.write_text(f.read_text() + "\nRead `../../agents/skit-critic.md`.\n")
        self.assertTrue(any("agents folder" in p for p in self.problems()))

    def test_lint_requires_the_skit_prefix_on_a_skill(self):
        (self.tmp / "skills" / "skit-bro").rename(self.tmp / "skills" / "soti-bro")
        f = self.tmp / "skills" / "soti-bro" / "SKILL.md"
        f.write_text(f.read_text().replace("name: skit-bro", "name: soti-bro"))
        self.assertTrue(any("soti-bro" in p and "bad skill name" in p for p in self.problems()))

    def test_lint_requires_the_skit_prefix_on_an_agent(self):
        (self.tmp / "agents" / "skit-builder.md").rename(self.tmp / "agents" / "soti-builder.md")
        f = self.tmp / "agents" / "soti-builder.md"
        f.write_text(f.read_text().replace("name: skit-builder", "name: soti-builder"))
        self.assertTrue(any("soti-builder" in p and "start with skit-" in p for p in self.problems()))

    def test_plugin_and_marketplace_are_named_skit(self):
        import json
        plugin = json.loads((REPO / ".claude-plugin" / "plugin.json").read_text())
        market = json.loads((REPO / ".claude-plugin" / "marketplace.json").read_text())
        self.assertEqual(plugin["name"], "skit")
        self.assertEqual(market["name"], "skit")
        self.assertEqual([p["name"] for p in market["plugins"]], ["skit"])

    def set_version(self, name, version):
        import json
        f = self.tmp / ".claude-plugin" / name
        data = json.loads(f.read_text())
        if name == "marketplace.json":
            data["plugins"][0]["version"] = version
        else:
            data["version"] = version
        f.write_text(json.dumps(data))

    def test_plugin_declares_no_version_so_it_tracks_commits(self):
        self.assertNotIn("version", " ".join(self.problems()))

    def test_lint_rejects_a_version_in_plugin_json(self):
        self.set_version("plugin.json", "1.0.2")
        self.assertTrue(any("plugin.json" in p and "version" in p for p in self.problems()))

    def test_lint_rejects_a_version_in_marketplace_json(self):
        self.set_version("marketplace.json", "1.0.2")
        self.assertTrue(any("marketplace.json" in p and "version" in p for p in self.problems()))

    def test_vibe_ships_the_critic_rules_in_the_skill(self):
        self.assertTrue((REPO / "skills" / "skit-vibe" / "references" / "critic.md").is_file())

    def test_lint_rejects_critic_rules_that_drifted_from_the_agent(self):
        f = self.tmp / "skills" / "skit-vibe" / "references" / "critic.md"
        f.write_text(f.read_text() + "\nExtra rule.\n")
        self.assertTrue(any("critic rules differ" in p for p in self.problems()))


if __name__ == "__main__":
    unittest.main()

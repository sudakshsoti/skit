#!/usr/bin/env python3
"""Check every skill and agent before it ships.

Rules:
- Each skills/<dir>/SKILL.md has frontmatter whose `name` equals <dir>, is
  lowercase kebab-case, starts with `soti-`, and contains neither "claude" nor
  "anthropic". `description` is present and at most 1024 characters.
- Each agents/<file>.md has frontmatter whose `name` equals the file stem and
  starts with `soti-`.
- Every backticked `soti-*` name in a skill or agent resolves to a skill or
  agent in this repo, so nothing points at a skill a user won't have.
- Relative links and `references/...` paths inside a skill resolve.
- No file contains a personal detail from BLOCKLIST, or harness-local syntax
  that only works on the author's machine.
- README.md documents every skill on disk.

Exit 1 with one line per problem; print "ok" otherwise.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
AGENTS = ROOT / "agents"

BLOCKLIST = [
    r"\bSudaksh\b(?! Soti\b)",  # the author name is allowed only in full, in metadata
    r"\bOptum\b",
    r"\bGurugram\b",
    r"skill://",
    r"~/\.(omp|pi|agents|claude)\b",
    r"/Users/",
    r"\bagent-config\b",
    r"\b[0-9a-f]{40}\b",  # commit hashes
]
BLOCK_RE = [re.compile(p) for p in BLOCKLIST]
NAME_RE = re.compile(r"^soti-[a-z0-9]+(-[a-z0-9]+)*$")
REF_RE = re.compile(r"`(soti-[a-z0-9-]+)`")
PATH_RE = re.compile(r"`((?:\.\./)*(?:references|templates|examples|agents)/[A-Za-z0-9_./-]+\.md)`")


def frontmatter(text: str) -> dict[str, str]:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    out: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip().strip('"')
    return out


def main() -> int:
    problems: list[str] = []
    skills = sorted(p.name for p in SKILLS.iterdir() if p.is_dir())
    agents = sorted(p.stem for p in AGENTS.glob("*.md"))
    known = set(skills) | set(agents)

    for name in skills:
        f = SKILLS / name / "SKILL.md"
        if not f.exists():
            problems.append(f"{f.relative_to(ROOT)}: missing")
            continue
        fm = frontmatter(f.read_text())
        if fm.get("name") != name:
            problems.append(f"{f.relative_to(ROOT)}: name {fm.get('name')!r} != directory {name!r}")
        if not NAME_RE.match(name) or "claude" in name or "anthropic" in name:
            problems.append(f"{f.relative_to(ROOT)}: bad skill name {name!r}")
        desc = fm.get("description", "")
        if not desc:
            problems.append(f"{f.relative_to(ROOT)}: missing description")
        elif len(desc) > 1024:
            problems.append(f"{f.relative_to(ROOT)}: description is {len(desc)} chars (max 1024)")

    for name in agents:
        f = AGENTS / f"{name}.md"
        fm = frontmatter(f.read_text())
        if fm.get("name") != name or not NAME_RE.match(name):
            problems.append(f"{f.relative_to(ROOT)}: agent name {fm.get('name')!r} must equal {name!r} and start with soti-")

    for f in sorted(list(SKILLS.rglob("*.md")) + list(AGENTS.glob("*.md"))):
        text = f.read_text()
        rel = f.relative_to(ROOT)
        for i, line in enumerate(text.splitlines(), 1):
            for rx in BLOCK_RE:
                if rx.search(line):
                    problems.append(f"{rel}:{i}: blocked pattern {rx.pattern!r}")
            for ref in REF_RE.findall(line):
                if ref not in known:
                    problems.append(f"{rel}:{i}: `{ref}` is not a skill or agent in this repo")
            for path in PATH_RE.findall(line):
                base = f.parent
                # paths in SKILL.md are relative to the skill dir; in references, try both
                candidates = [base / path, base.parent / path]
                if not any(c.resolve().exists() for c in candidates):
                    problems.append(f"{rel}:{i}: path `{path}` does not exist")

    readme = (ROOT / "README.md").read_text() if (ROOT / "README.md").exists() else ""
    for name in skills:
        if f"`{name}`" not in readme:
            problems.append(f"README.md: skill `{name}` is not documented")

    for p in problems:
        print(p)
    if not problems:
        print("ok")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

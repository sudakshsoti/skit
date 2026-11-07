#!/usr/bin/env python3
"""Check every skill and agent before it ships.

Rules:
- Each skills/<dir>/SKILL.md has frontmatter whose `name` equals <dir>, is
  lowercase kebab-case, starts with `skit-`, and contains neither "claude" nor
  "anthropic". `description` is present and at most 1024 characters.
- No skill or agent here starts with `soti-`: that prefix is personal and lives
  in the owner's agent-config repo, so a `soti-` name fails with its own message.
- Each agents/<file>.md has frontmatter whose `name` equals the file stem and
  starts with `skit-`.
- Every backticked `skit-*` name in a skill or agent resolves to a skill or
  agent in this repo, so nothing points at a skill a user won't have.
- Relative links and `references/...` paths inside a skill resolve.
- No file contains a personal detail from BLOCKLIST, or harness-local syntax
  that only works on the author's machine.
- README.md documents every skill on disk.
- `skit-ux-copy` and `skit-handoff` start automatically: other skills hand work
  to them, and a manual-only skill cannot be loaded by the model.
- Each job has one named owner, and the descriptions agree: `skit-vibe` and
  `skit-interface` name each other (build vs review), as do `skit-grilling` and
  `skit-design-grill` (general vs design grill).
- No skill points into the agents folder. A skill must work when only skills
  are installed, so the rules an agent carries are also shipped in the skill:
  `skit-vibe/references/critic.md` must match the body of `agents/skit-critic.md`.
- `skit-vibe` carries a move table: each move appears once and names a skill
  that exists here, so a request phrased as a move loads one owner.

Exit 1 with one line per problem; print "ok" otherwise.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Skills other skills depend on, so the model must be able to start them.
AUTO_START = ("skit-ux-copy", "skit-handoff")
# Skills whose descriptions must route to each other, so each job has one owner.
ROUTES = {
    "skit-vibe": "skit-interface",
    "skit-interface": "skit-vibe",
    "skit-grilling": "skit-design-grill",
    "skit-design-grill": "skit-grilling",
}
# Personal skills live in the owner's agent-config repo; shared ones start `skit-`.
PERSONAL_PREFIX = "soti-"
AGENT_PATH_RE = re.compile(r"(?:\.\./)+agents/|`agents/")

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
NAME_RE = re.compile(r"^skit-[a-z0-9]+(-[a-z0-9]+)*$")
REF_RE = re.compile(r"`(skit-[a-z0-9-]+)`")
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


def body(text: str) -> str:
    return re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.S).strip()


MOVE_HEADER_RE = re.compile(r"^\|\s*Move\s*\|\s*Owner\s*\|\s*$")


def lint_moves(vibe: Path, root: Path, skills: set[str]) -> list[str]:
    """Each move in skit-vibe's move table appears once and names a real skill."""
    rel = vibe.relative_to(root)
    lines = [line.strip() for line in vibe.read_text().splitlines()]
    start = next((i for i, line in enumerate(lines) if MOVE_HEADER_RE.match(line)), None)
    if start is None:
        return [f"{rel}: no move table (a `| Move | Owner |` table in the quick-tweak route)"]
    problems: list[str] = []
    seen: set[str] = set()
    for line in lines[start + 2:]:
        if not line.startswith("|"):
            break
        cells = [c.strip() for c in line.strip("|").split("|")]
        moves, owner = cells[0], cells[1] if len(cells) > 1 else ""
        m = re.fullmatch(r"`(skit-[a-z0-9-]+)`", owner)
        for move in (x.strip() for x in moves.split(",") if x.strip()):
            if move in seen:
                problems.append(f"{rel}: move {move!r} appears more than once in the move table")
            seen.add(move)
            if not m or m.group(1) not in skills:
                problems.append(f"{rel}: move {move!r} names {owner or 'no owner'}, which is not a skill in this repo")
    return problems


def lint(root: Path) -> list[str]:
    SKILLS = root / "skills"
    AGENTS = root / "agents"
    problems: list[str] = []
    skills = sorted(p.name for p in SKILLS.iterdir() if p.is_dir())
    agents = sorted(p.stem for p in AGENTS.glob("*.md"))
    known = set(skills) | set(agents)

    for name in skills:
        f = SKILLS / name / "SKILL.md"
        if not f.exists():
            problems.append(f"{f.relative_to(root)}: missing")
            continue
        fm = frontmatter(f.read_text())
        if fm.get("name") != name:
            problems.append(f"{f.relative_to(root)}: name {fm.get('name')!r} != directory {name!r}")
        if name.startswith(PERSONAL_PREFIX):
            problems.append(f"{f.relative_to(root)}: {name!r} uses the personal prefix {PERSONAL_PREFIX!r}; personal skills live in agent-config, shared skills here start with skit-")
        elif not NAME_RE.match(name) or "claude" in name or "anthropic" in name:
            problems.append(f"{f.relative_to(root)}: bad skill name {name!r}")
        desc = fm.get("description", "")
        if not desc:
            problems.append(f"{f.relative_to(root)}: missing description")
        elif len(desc) > 1024:
            problems.append(f"{f.relative_to(root)}: description is {len(desc)} chars (max 1024)")

    for name in agents:
        f = AGENTS / f"{name}.md"
        fm = frontmatter(f.read_text())
        if name.startswith(PERSONAL_PREFIX):
            problems.append(f"{f.relative_to(root)}: {name!r} uses the personal prefix {PERSONAL_PREFIX!r}; personal agents live in agent-config, shared agents here start with skit-")
        elif fm.get("name") != name or not NAME_RE.match(name):
            problems.append(f"{f.relative_to(root)}: agent name {fm.get('name')!r} must equal {name!r} and start with skit-")

    for f in sorted(list(SKILLS.rglob("*.md")) + list(AGENTS.glob("*.md"))):
        text = f.read_text()
        rel = f.relative_to(root)
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

    readme = (root / "README.md").read_text() if (root / "README.md").exists() else ""
    for name in skills:
        if f"`{name}`" not in readme:
            problems.append(f"README.md: skill `{name}` is not documented")

    for name in AUTO_START:
        f = SKILLS / name / "SKILL.md"
        if f.exists() and "disable-model-invocation" in frontmatter(f.read_text()):
            problems.append(f"{f.relative_to(root)}: must start automatically (remove disable-model-invocation)")

    for name, other in ROUTES.items():
        f = SKILLS / name / "SKILL.md"
        if f.exists() and other not in frontmatter(f.read_text()).get("description", ""):
            problems.append(f"{f.relative_to(root)}: description must route to {other}")

    for f in sorted(SKILLS.rglob("*.md")):
        for i, line in enumerate(f.read_text().splitlines(), 1):
            if AGENT_PATH_RE.search(line):
                problems.append(f"{f.relative_to(root)}:{i}: points into the agents folder, which a skills-only install lacks")

    vibe = SKILLS / "skit-vibe" / "SKILL.md"
    if vibe.exists():
        problems.extend(lint_moves(vibe, root, set(skills)))

    skill_critic = SKILLS / "skit-vibe" / "references" / "critic.md"
    agent_critic = AGENTS / "skit-critic.md"
    if skill_critic.exists() and agent_critic.exists():
        if body(skill_critic.read_text()) != body(agent_critic.read_text()):
            problems.append(
                f"{skill_critic.relative_to(root)}: critic rules differ from {agent_critic.relative_to(root)}; keep the two identical"
            )
    elif (SKILLS / "skit-vibe").exists():
        problems.append("skills/skit-vibe/references/critic.md: missing (skit-vibe must carry the critic rules)")

    # No version anywhere: Claude Code then uses the commit SHA, so every push
    # reaches installed plugins. A pinned version would freeze users on a cached copy.
    manifests = root / ".claude-plugin"
    for fname in ("plugin.json", "marketplace.json"):
        f = manifests / fname
        if not f.exists():
            continue
        data = json.loads(f.read_text())
        entries = [data] + [e for e in data.get("plugins", []) if isinstance(e, dict)]
        if any("version" in e for e in entries):
            problems.append(
                f".claude-plugin/{fname}: remove `version`; without one the plugin follows every commit"
            )

    return problems


def main() -> int:
    problems = lint(ROOT)
    for p in problems:
        print(p)
    if not problems:
        print("ok")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

---
name: skit-start
description: >-
  Find the skit skill, or the short path of several, that fits what the user is doing, then offer to run it.

  Triggers: "where do I start", "which skill do I need", "what skill fits this", "which skit skill should I use", "run the right skills for this".

  Not for doing one named skill's job when the request already matches it, such as building a screen (skit-vibe) or grilling a plan (skit-grilling).
---

# Start

The user does not have to remember every skit skill. Find the one that fits, or the short order of several, say why in plain words, and offer to run it. Until they say yes, this skill only answers: it does no design or review work of its own, so the user stays in charge of what happens next.

## 1. Find the task

Take it from the user's message first. When the message names no task, work it out from the conversation so far, then from the changed files (`git status`, `git diff`) or the files just discussed, and state the task you inferred in one line so they can correct it. When there is still nothing to go on, ask one question: "What are you working on?"

## 2. Choose the skill or path

[references/map.md](references/map.md) lists every skit skill with how it starts, its job and what it is not for, plus the usual paths. Use it to orient, then read each chosen skill's own SKILL.md before you describe it, because the map is a summary and the skill is the source of truth.

Choose on your own when one route is clearly better. Ask the user only when two routes would lead to materially different work, for example restyling a screen against reviewing it for faults; ask one question and put your recommendation first.

## 3. Answer

Open with the answer on one line: the single skill, or the path as "skit-design-grill, then skit-visual-design, then skit-vibe". Then one plain line per skill: why it fits here, and how it starts.

- **auto** skills start on their own when a request matches.
- **manual** skills start only when typed: `/skit:<name>` in Claude Code, or by asking for the skill by name elsewhere.

When two skills could fit, name the better one first and say what would change the pick. Finish by asking whether to run the path now.

## 4. Run it, if the user says yes

Load each skill in order and do the task following it, finishing one skill's work before opening the next, so each hand-off starts from a finished result. A skill that turns out not to apply is dropped, with one line saying so.

A manual skill cannot be loaded through the skill tool, so read its `SKILL.md` from the folder beside this one (`../<name>/SKILL.md`) and follow it.

End with the outcome in plain words, then the skills used, then anything left for the user to decide.

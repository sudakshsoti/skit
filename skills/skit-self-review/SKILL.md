---
name: skit-self-review
description: >-
  Check your own build plan against a fixed list and fix it before building.

  Triggers: "is this plan sound", "check your plan", "what does this plan assume", "is this overkill", "will this break anything"; also right after you propose a plan bigger than a step or two.

  Not for trivial single-step plans, code diffs, or frontend code quality (skit-maintainability-review).
user-invocable: true
---

# Plan self-review

Critique the plan you just proposed, then revise it, in the current session.

Answer every checklist item against your own plan, or write "none":

1. Unstated assumptions, and what breaks if each is false.
2. Internal inconsistencies: where the plan contradicts itself or a stated
   requirement.
3. Blind spots that apply: auth, race conditions, migration and
   rollback, error handling, idempotency, tests, data loss, observability.
4. Over-engineering: where it exceeds the problem. Give the simpler version.
5. Verdict: ship / fix / rethink, then the top three changes.

Then revise the plan to address every point. For any point you reject, give a
one-line reason. Show what changed, not the whole plan again.

## Dispatch

If the plan touches more than 5 files or spans several workstreams, give the
checklist above to a fresh subagent on the session's own model (a general-purpose
subagent in Claude Code, the `general-purpose` agent in
Pi), so the critique comes from a clean context rather than the one that wrote
the plan.

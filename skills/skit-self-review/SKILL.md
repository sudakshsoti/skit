---
name: skit-self-review
description: "Use immediately after proposing a non-trivial engineering plan or when a self-review is requested; critique your own plan against a fixed checklist and revise it to address every point. Not for trivial single-step plans, code diffs, or frontend code quality (skit-maintainability-review)."
user-invocable: true
---

# Plan check

Critique the plan you just proposed, then revise it, in the current session.

Answer every checklist item against your own plan, or write "none":

1. Unstated assumptions, and what breaks if each is false.
2. Internal inconsistencies: where the plan contradicts itself or a stated
   requirement.
3. Blind spots that genuinely apply: auth, race conditions, migration and
   rollback, error handling, idempotency, tests, data loss, observability.
4. Over-engineering: where it exceeds the problem. Give the simpler version.
5. Verdict: ship / fix / rethink, then the top three changes.

Then revise the plan to address every point. For any point you reject, give a
one-line reason. Show what changed, not the whole plan again.

## Dispatch

If the plan touches more than 5 files or spans several workstreams, give the
checklist above to a fresh subagent on the session's own model (a general-purpose
subagent in Claude Code, a `task` subagent in OMP, the `general-purpose` agent in
Pi), so the critique comes from a clean context rather than the one that wrote
the plan.

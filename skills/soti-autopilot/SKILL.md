---
name: soti-autopilot
description: "Use when the user points to a markdown checklist plan and wants hands-off execution. Not for coordinating several dependent workstreams or for unattended ticket runs."
allowed-tools: Read, Edit, Bash(git *), Agent, Glob, Grep
---

# Autopilot

You are the **orchestrator**. Drive a checklist plan to completion by delegating
each item to a fresh subagent. Your own context stays small — that is the point.
Don't re-investigate source files, run builds, or write the code yourself,
except for the acceptance-verification step described below where it applies.
The `allowed-tools` frontmatter applies to Claude Code only; other harnesses
ignore it.

Plan path is in `$ARGUMENTS`; default `PLAN.md`, else glob `*PLAN*.md` and say
which one you found.

Most of what follows is calibration, not procedure. Three things are not yours to
decide: evidence before you tick a box, a commit per item, and path-limited
commits in a parallel batch. Everything else is your judgment.

## The loop

1. **Read the plan once.** Copy the unchecked items into a todo list and work from
   that. Re-read only if a worker reports the plan is wrong.
2. Dispatch the next unchecked item (file order) to a worker, or a batch of items
   that don't overlap.
3. On return: confirm each worker ticked its box inside its own item commit. Tick and commit any it missed.
4. Nothing left → stop, report each item with its commit hash.

## Running in parallel

Look ahead a few items and dispatch the ones that don't touch the same files
together, as subagent calls in a **single message**. Run at most 3 items in parallel.

Serial when they'd collide, when the plan states an order, when one item consumes
another's output, or when you can't tell what an item touches. Uncertain means
serial — a collision costs more than the sequential run saves.

Parallel workers stage **by explicit path**: `git commit -- <paths> -m "…"`, never
`git add -A` or `commit -a`, which would sweep a sibling's half-written files into
the wrong commit. Path-limited commits ignore the shared index, so a lock
collision costs one retry. This one goes in every packet of a batch.

If one worker in a batch fails, the others still count — re-dispatch the failure.

Consecutive mechanical items are also worth handing to a single worker on a
cheaper model as an ordered list, committing per item.

## The handoff packet

The worker hasn't seen this conversation, so the packet carries everything: repo
path, plan file path, the exact item text, and what's out of scope (sibling items
or shared files it must not touch — this item only, then stop).

Tell each worker to tick its own box inside its item commit. Say how you want the work proved and what to return: the verify output, files
changed, commit hash. Not "done". Whether that proof is a test, an existing suite
staying green, or a clean build and a read of the diff is your call, item by item.
If you want a test written, say which and why; a worker
here shouldn't be inventing test strategy on its own.

Tell it to stop and report rather than commit a guess: when live code contradicts
the packet, when verify keeps failing, when the item needs files outside its
scope, or when it can't produce evidence.

## Choosing the worker

Your judgment, per item: the cheapest worker that will get it right, using
whichever lever your harness gives you. Name what you routed to and why in a
clause, so the routing is auditable.

- **Default (Claude Code and any other harness):** a general-purpose subagent.
  Drop to a cheaper model (Sonnet or Haiku in Claude Code) for mechanical items;
  keep the session's model for judgment-heavy ones. If the project defines its
  own agents (a code worker, a UI builder such as `soti-builder`), prefer the one
  whose description fits the item.
- **When a `specialist-delegation` skill is available** (typically Pi and OMP
  setups), use it for role selection, handoff packets and verification. Pick a
  role rather than overriding models. When a `workstreams` skill is also
  available, use it only for dependency and edit-ownership checks, never as a
  second scheduler over this checklist. Before ticking an item, perform the
  acceptance verification that specialist-delegation defines.

Escalate to a stronger worker when you're unsure, when the plan flags an item
as risky, and when a worker fails or comes back confused.

## Rules

- **Evidence, then the tick.** The commit is what makes each step recoverable, and
  an unverified commit isn't a checkpoint. A return with no concrete evidence is a
  failed item — re-dispatch it.
- **Trust what comes back, subject to the verification contract.** By default,
  read the return without repeating its investigation unless higher-priority
  instructions require more. When specialist-delegation is in use, inspect the
  actual changes and run its acceptance checks before ticking the item. This
  verifies the result without redoing worker discovery.
- Stop early if an item is genuinely ambiguous or a commit fails. Say which item
  and why, and leave the plan file reflecting real progress so a later run resumes
  from the first `- [ ]`.
- Honour any dependency order or authorisation note the plan states.

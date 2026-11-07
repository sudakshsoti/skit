---
name: skit-vibe
description: "Use to build any interface change (tweak, new screen, risky UI/data change): it owns building UI, choosing process depth and running build-review. Not for non-UI work, or for reviewing or critiquing an existing UI (skit-interface); visual direction and type come from skit-visual-design and skit-type."
---

# Vibe

This skill is a workflow, not an aesthetic. It decides how much process an interface task needs and holds the build to a rendered, reviewed result. Visual language, tokens and review thresholds come from `skit-interface`, `skit-visual-design`, `skit-type` and `skit-ux-copy`. Do not duplicate their guidance here.

## 1. Pick the route

1. **Quick tweak.** One component or style area; none of the Builder's quick-tweak escalations (`skit-builder` agent) apply. Inspect the current screen, tokens and nearest comparable pattern, then build without an approval pause unless the request conflicts with a `[stated]` decision (a settled line in the project's `design/decisions.md`, written by `skit-design-grill`).

   When the request names a move (a kind of design change, such as "make the pricing cards quieter" or "harden checkout"), load the move's owner before building and follow its guidance. Each move has exactly one owner:

   | Move | Owner |
   | --- | --- |
   | bolder, quieter, distill, colorize, animate | `skit-visual-design` |
   | typeset | `skit-type` |
   | layout, harden | `skit-interface` |
   | clarify | `skit-ux-copy` |

   Polish is not a move. `skit-polish` runs only when the user calls it by name; when a request asks for a finishing pass, build what it names and point the user to `skit-polish`.

2. **Shape first.** A new screen, changed workflow, unclear hierarchy or competing direction. If `design/decisions.md` has no settled direction, run `skit-design-grill` in the main session. Then run the Plan role and present the single decision that changes the work. Wait for approval before building. A new standalone page is always this route; use the active design skills directly.
3. **Risky change.** Authentication, persistent data, dependencies, destructive operations, migrations or broad architecture. Run the Plan role, explain the impact and rollback shape, and wait for explicit approval before implementation.

## 2. Roles and the hand-off contract

Three roles. Each agent file defines its own return shape; the next role starts from that, not from the conversation.

- **Plan** returns confirmed decisions, exact files, target viewports, required states, checks to run and unresolved questions.
- **Builder** receives that hand-off or an explicitly bounded quick tweak. See the `skit-builder` agent for its boundary and return.
- **Critic** receives the screenshots, the project-local audit output (or `audit didn't run`) and the relevant implementation. Its rules and return shape (prioritised findings, named coverage, `ship` or `fix`) live in the `skit-critic` agent and in `references/critic.md`, because it runs without loading this skill. Do not restate them in the dispatch.

How the roles run depends on the harness. In Claude Code with this plugin, Plan runs in the main session (or plan mode), Builder is the `skit-builder` subagent, and Critic is a fresh `skit-critic` subagent given the absolute screenshot paths. In another harness, or in Claude Code without the plugin's agents, use its planner, builder and reviewer roles if it has them; otherwise run Plan and Builder in the main session and Critic in a fresh subagent. That Critic is told to read and follow `references/critic.md` in this skill's folder, which holds the same rules as the `skit-critic` agent. Give it the absolute path to that file.

When a role runs in the main session, still write its output in the role's shape before moving on. The Critic must run in a fresh context: a session reviewing its own build approves it. If no image-capable reviewer exists, report "Critic pass unavailable" and do not claim visual quality.

## 3. Rendered or not done

A visual change is not complete until its rendered result has been inspected. If no runnable app, URL, representative state or browser path exists, name the blocker and do not claim visual success. When responsiveness can change, inspect both narrow and wide viewports. Run the project-local audit below before the Critic.

If the Critic returns `fix`, dispatch the Builder for one focused repair, capture fresh screenshots, re-run the project-local audit and run the Critic once more. If the second verdict is still `fix`, stop and ask the user.

### Project-local audit

The project-local audit is Impeccable's detector, used through its command line and nothing else. Keep the Impeccable skill and its hooks out of a skit project: two design-skill packs give conflicting guidance, and the hooks run outside model approval. Run every scan with `npx --no-install`, so a missing detector fails instead of downloading.

1. Scan the changed source: `npx --no-install impeccable detect --json <changed files>`.
2. When a dev server is running, also scan the page URL twice: `--viewport 390x844` for phone width, where sideways overflow shows, and `--viewport 1440x900` for desktop.
3. Read each exit code. `0` is clean and `2` means findings; both hand the full JSON from standard output to the Critic, advisory entries included. `1` means at least one target could not be scanned, even when other targets produced findings: report that scan as `audit didn't run` with the reason from standard error, and still pass on any JSON it printed. When npx says the package is missing, every scan is `audit didn't run`, and the build carries on.

The audit is done when each scan has one result: clean, findings passed to the Critic, or `audit didn't run`. A scan that exits `1` is never reported as clean. Leave the detector's own ignore config alone: the Critic drops the findings a stated exception in `design/decisions.md` covers.

## 4. Final report

Finish with user-visible changes, screenshot paths, each audit scan's result (clean, the finding count, or `audit didn't run` and why), the Critic's verdict, changed files and any unresolved risk.

# skit skill map

Every skit skill, with how it starts. **auto** starts on its own when a request matches; **manual** starts only when its name is typed. Read a skill's own SKILL.md before saying what it does: this map is for orientation.

## Usual paths

- A new screen: **skit-design-grill** (only if the look and behaviour are undecided), then **skit-visual-design** and **skit-type** as needed, then **skit-vibe**, which builds, renders and reviews it.
- Improve an existing screen: **skit-interface** (finds what is wrong), then **skit-vibe** to fix it, then **skit-polish** for the last details.
- The words on a screen: **skit-ux-copy**.
- A product idea or business case: **skit-strategy**, then **skit-design-grill** once it turns into screens.
- A plan or decision: **skit-grilling** to settle it, then **skit-self-review** once a build plan exists, then **skit-autopilot** if it is a checklist to run hands-off.
- Code an agent wrote: **skit-maintainability-review**.
- End of a session: **skit-handoff**. An answer that was hard to read: **skit-bro**.

## Design

- **skit-strategy** (auto): Product and UX strategy: business model, positioning, journey maps, teardowns, stakeholder notes.
  - Not for visual direction (skit-visual-design), interface states (skit-interface) or screen design decisions (skit-design-grill).
- **skit-design-grill** (auto): Settle how a screen looks and behaves, by interview; decisions go to `design/decisions.md`.
  - Not for a plan, decision or idea that is not an interface (skit-grilling).
- **skit-visual-design** (auto): Visual direction: colour, hierarchy, responsive layout and CSS tokens.
  - Not for typography-primary work (skit-type), behaviour and states (skit-interface), or building the change (skit-vibe).
- **skit-type** (auto): Choose and pair typefaces, size them, and fix loading and script coverage.
  - Not for general UI styling (skit-visual-design) or copy (skit-ux-copy).
- **skit-interface** (auto): Review controls, forms, lists and screen states: labels, focus, hit areas, the states people forget.
  - Not for building a UI change (skit-vibe) or visual styling (skit-visual-design).
- **skit-ux-copy** (auto): Write or check button labels, errors, empty states, onboarding and notifications.
  - Not for long-form prose, or visual and type decisions.
- **skit-vibe** (auto): Build any UI change, render it in a browser and have it reviewed before calling it done.
  - Not for non-UI work or reviewing an existing UI (skit-interface).
- **skit-polish** (manual): A finishing pass for a page whose direction is right but still feels unfinished.
  - Not for hierarchy and layout problems (skit-interface) or visual direction (skit-visual-design).

## Planning and review

- **skit-grilling** (auto): Interview the user until nothing in a plan, decision or idea is a guess.
  - Not for visual or behavioural interface decisions (skit-design-grill).
- **skit-self-review** (auto): Check a build plan against a fixed checklist and revise it before building.
  - Not for code diffs or frontend code quality (skit-maintainability-review).
- **skit-maintainability-review** (manual): Review AI-written frontend code for whether a person could maintain it.
  - Not for reviewing a plan before building (skit-self-review).
- **skit-autopilot** (manual): Work through a markdown checklist plan hands-off, verifying and committing each item.
  - Not for settling what the plan should be (skit-grilling).

## Session helpers

- **skit-handoff** (auto): Write a handoff so the next session picks up where this one stopped.
  - Not for issue-tracker upkeep or personal task capture.
- **skit-bro** (manual): Restate the agent's last message in plain words.
  - Not for rewriting interface text (skit-ux-copy).

# soti

Skills for designing and building interfaces with an AI coding agent, plus a few for keeping plans and code honest.

They tell the agent what a careful designer and reviewer would do: settle the decisions before building, pick the right type, cover the error and empty states, write the button labels properly, look at the rendered result, and catch code that a human will struggle to maintain.

Works with Claude Code, Codex, Cursor, and any other agent that reads `SKILL.md` skills.

## Install

### Claude Code (recommended)

```
/plugin marketplace add sudakshsoti/soti-skills
/plugin install soti@soti
```

That installs every skill and the two helper agents.

**Getting updates.** Claude Code doesn't auto-update marketplaces you add yourself. Turn it on once: run `/plugin`, open **Marketplaces**, choose **soti** and enable auto-update. New releases then arrive when Claude Code starts. Without it, run `/plugin marketplace update soti` whenever you want the latest.

### Codex, Cursor and other agents

```
npx skills add sudakshsoti/soti-skills
```

Update later with `npx skills update`. The helper agents are Claude Code only; the skills fall back to doing the work themselves when the agents aren't there.

### claude.ai

Download this repo, zip any skill folder from `skills/` (for example `skills/soti-type`), and upload it under **Settings → Capabilities → Skills**. claude.ai doesn't update uploaded skills, so re-upload when a new release comes out.

## How the skills fit together

You don't have to use them in order; each one works alone. But for a new screen they line up like this:

```mermaid
flowchart LR
    G[soti-design-grill<br/>settle the decisions] --> A[soti-art-direction<br/>colour, layout, tokens]
    G --> T[soti-type<br/>typefaces]
    G --> I[soti-interface<br/>controls and states]
    G --> C[soti-ux-copy<br/>the words]
    A --> V[soti-vibe<br/>build, render, review]
    T --> V
    I --> V
    C --> V
    V --> S[soti-slop-check<br/>is the code maintainable?]
```

Decisions you agree on during a grill are written to `design/decisions.md` in your project. The other skills read that file, so the agent doesn't re-ask or quietly override what you settled. A skill creates the file the first time it needs it.

## The skills

Most skills start on their own when your request matches. The ones marked **manual** only run when you call them: type `/soti:<skill-name>` in Claude Code, or ask for the skill by name elsewhere.

### Design

**`soti-design-grill`**: an interview, in rounds, that settles what a screen should look like and how it should behave before anything gets built. It sticks to visible decisions (layout, states, copy, motion) and leaves code architecture alone.
> "Grill me on the design of the onboarding flow before we build it."

**`soti-art-direction`**: visual direction for a product UI. It first works out what kind of surface this is (a dense tool, a marketing page, a dashboard), then sets colour in OKLCH, hierarchy, responsive layout and CSS tokens to match. Uses Emil Kowalski's animation skill for motion if you have it installed, and its own motion notes otherwise.
> "Give this settings app a visual direction. It feels flat and generic."

**`soti-type`**: choosing typefaces and pairings, OpenType features, font loading, and coverage for other languages and scripts, for screen, print or brand work.
> "Pick a type pairing for a finance dashboard that also has to render Hindi."

**`soti-interface`**: the behaviour of controls, forms, lists, dashboards and settings: structure, labels, focus order, hit areas, and every field state. It is strict about the screens people forget: loading, empty, error, partial and offline.
> "Review this signup form. What states am I missing?"

**`soti-ux-copy`** (manual): writing and auditing interface text: buttons, form labels, errors, empty states, onboarding, notifications, voice and tone. Comes with templates for the common cases.
> "/soti:soti-ux-copy rewrite the error messages on the payment screen"

**`soti-vibe`**: the build loop for any interface change. It sizes the change first, so a colour tweak gets a quick pass and a new screen gets a plan, then builds, renders the result in a browser and reviews the screenshot before calling it done. In Claude Code it hands the build to the `soti-builder` agent and the review to `soti-critic`.
> "Add a filter bar to the orders table."

### Planning and review

**`soti-grilling`**: a general version of the design grill for any plan, decision or idea. It asks a few sharp questions per round, using your agent's question picker when it has one, until nothing important is left assumed. Inspired by Matt Pocock's `grilling` skill.
> "Grill me on this migration plan."

**`soti-plan-check`**: after the agent proposes a non-trivial plan, it critiques the plan against a fixed checklist (unstated assumptions, contradictions, blind spots like rollback and data loss, over-engineering) and revises it.
> "Check that plan before you start."

**`soti-slop-check`** (manual): reviews AI-written frontend code for whether a person can maintain it: duplication, needless abstractions, vague names, silent failures, and drift between sessions.
> "/soti:soti-slop-check src/components"

**`soti-autopilot`**: works through a markdown checklist plan without stopping to ask, ticking items off, verifying each one and committing as it goes. It uses subagents where your tool has them.
> "Run plans/dark-mode.md on autopilot."

### Session helpers

**`soti-handoff`** (manual): writes a structured handoff (decisions, progress, changed files, next steps) so the next session can pick up where this one stopped.
> "/soti:soti-handoff"

**`soti-bro`** (manual): restates the agent's last message in plain words, for when the answer was correct but dense.
> "/soti:soti-bro"

## Agents (Claude Code)

- **soti-builder** implements an approved UI plan or a small tweak in React, shadcn/ui, Tailwind CSS or plain HTML, and returns screenshots as evidence.
- **soti-critic** is a read-only reviewer: it looks at screenshots and the implemented UI and returns ranked findings with a ship-or-fix verdict.

`soti-vibe` uses both. You can also call them directly.

## Feedback

Bug reports and suggestions are welcome as [issues](https://github.com/sudakshsoti/soti-skills/issues). Pull requests are by invitation: open an issue first.

## Licence

[MIT](LICENSE) © Sudaksh Soti

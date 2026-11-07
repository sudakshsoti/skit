---
name: skit-polish
description: "A finishing pass, run by name, for a page whose direction is right but still feels unfinished: hover shifts, press feedback, punctuation, and the small details other skills own."
user-invocable: true
disable-model-invocation: true
---

# Polish

A finishing pass over a page whose direction is settled and right, but which still feels unfinished. It changes small details only. A problem with hierarchy, layout or visual direction is not polish: name it and hand it back to `skit-vibe`.

Each detail has one owner. Where another skill already holds the rule, this pass names the check and sends you to that rule; it holds rules only for the details nobody else owns.

## Steps

1. Render the page at 390 and 1440 CSS pixels wide, or use the screenshots from the last `skit-vibe` build. Hover, press, focus and select every control on it.
2. Walk every check in the two lists below. For a check with an owner, read that owner's rule and apply it as written.
3. Fix what fails in the project's own styling system and tokens, then render again and look.
4. Report each check by name as passed, fixed (with `file:line`) or not applicable.

The pass is done when every check below has one of those three results.

## Checks another skill owns

| Check | Where the rule lives |
| --- | --- |
| A visible focus ring on every control | `skit-interface`, Focus and keyboard |
| Hit areas large enough to press | `skit-interface`, its target-size reference |
| z-index and stacking | `skit-interface`, its layout, navigation and feedback reference |
| Skeletons shaped like the content they stand in for | `skit-interface`, its loading-states reference |
| Font smoothing, tabular numbers for changing values, truncation | `skit-type`, its Tailwind v4 mapping reference |
| Headings that wrap in balance | `skit-type`, the Wrapping rule in its screen-mechanics reference |
| All five interaction states on every control | `skit-visual-design`, Production visual system |
| Transitions that name only the properties that change | `skit-visual-design`, the Performance rule in its motion-values reference |

## Checks no other skill owns

**Weight stays put.** Hover, selected and active-tab states keep the font weight they rest at, and show the change through colour, background or an underline instead. A weight change widens the text and pushes its neighbours. When a selected state truly needs a heavier weight, reserve the heavier width in advance (a hidden copy of the label at that weight sets the box) so nothing moves. Check: hover and select each item and watch that nothing beside it shifts.

**A press answers.** A control shows it is being pressed while the pointer or finger is down: a slight scale-down on `:active`, around 0.97, or a darker fill when scaling would look wrong. It applies at once and releases quickly. The timing floor is `skit-interface`'s rule that a control acknowledges a press within 100ms. Check: press and hold each control and see it change.

**Real punctuation in UI copy.** Text the interface shows uses curly quotes and apostrophes (“ ” ‘ ’) and the single ellipsis character (…) rather than three full stops. Code samples, keyboard shortcuts and anything a user types or copies to paste keep straight characters. Check: search the changed UI strings for `'`, `"` and `...` inside visible text.

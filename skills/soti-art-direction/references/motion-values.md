# Motion values

When a dedicated motion skill is installed (for example `emil-animations`), it owns motion craft, including whether to animate at all, and the values below override its numbers. Without one, start from the baseline and use the values below as written.

## Baseline

- Animate only when motion explains a change: where something came from, where it went, or that an action registered. Frequent interactions (typing, row hovers, tab switches) get no animation or under `150ms`.
- Entrances `200-300ms` with an ease-out curve; exits shorter (see "Subtle exit").
- Animate `transform`, `opacity` and `filter`; leave layout properties (`width`, `height`, `top`) still.
- Honour `prefers-reduced-motion` with the table in "Reduced motion".

## Stagger timing

Stagger semantic chunks (title, description, buttons) at roughly `100ms` between groups. For a title split into individual words, stagger each word at roughly `80ms`. Never stagger routine, high-frequency interactions: row hovers, keystrokes, repeated tab changes. Reserve stagger for infrequent staged entrances where the sequence itself communicates hierarchy, such as a first-load page hero, a success state, or an empty state.

## Contextual icon swap

Animate an icon that changes contextually (hover, state toggle) with `opacity`, `scale` and `blur`, never by toggling visibility. Exact values, not a range:

- `scale`: `0.25` to `1`
- `opacity`: `0` to `1`
- `blur`: `4px` to `0`
- spring: `duration: 0.3, bounce: 0` — bounce is always `0` here, never `0.1` or any other value

Dependency-free CSS fallback where no motion library is installed: keep both icons in the DOM, one absolutely positioned over the other, and cross-fade with `transition-[opacity,filter,scale] duration-300 ease-[cubic-bezier(0.2,0,0,1)]`. The non-absolute icon defines the layout size; the absolute one overlays it without affecting flow. Never add a motion-library dependency solely for an icon swap.

## Subtle exit

`translateY(-12px)` over `150ms` `ease-out`. Exit duration is shorter than enter duration (`150ms` against `300ms`), since the user's attention is already moving to the next thing. Use a full slide (`translateX(-100%)` or similar) only where spatial context carries real meaning, such as a card returning to a list or a drawer closing; otherwise the subtle exit is the default.

## Theme-switch transition suppression

A theme flip changes `color`, `background`, `border` and `shadow` on nearly every element at once; every transition on those properties fires together and the switch smears instead of snapping.

1. Inject `*, *::before, *::after { transition: none !important }`.
2. Force a reflow by reading `document.body.offsetHeight` so the new theme resolves while the override is still applied.
3. Remove the override inside a nested `requestAnimationFrame` (one frame to let the reflow's paint land, one more to remove the rule after it), restoring transitions before the next interaction.

This is exactly what `next-themes`' `disableTransitionOnChange` does. An in-app toggle needs the same sequence around its own flip, not only the OS-level `prefers-color-scheme` change.

## Reduced motion: disable, replace, keep

| Disable | Replace with opacity crossfade | Keep |
| --- | --- | --- |
| Parallax | Slide transitions | Spinners |
| Autoplay | Scale transitions | Progress indicators |
| Large-scale movement | | Instant state changes |

## Performance

Tailwind's bare `transition` utility maps to a curated property list (colour, opacity, shadow, transform), not `all`; still name the exact properties changing (`transition-[scale,opacity]`) rather than relying on the bare utility. `transition-transform` in Tailwind maps to `transition-property: transform, translate, scale, rotate`, covering every transform-related property, not only `transform`.

Add `will-change` only for `transform`, `opacity` and `filter`, the properties the GPU can composite, and only after observing first-frame stutter, never preemptively on every animated element (each layer costs memory). `clip-path` is GPU-compositable only in newer Chromium and is not reliable enough cross-browser to justify `will-change` on it.

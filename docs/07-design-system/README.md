# Design System

The visual and interaction language of 2nd Brain.

> **Status** — ⬜ Finalised in Phase 5 alongside the dashboards. Principles and the token
> structure below are settled; the token values are provisional until then.

---

## Influences, and what is taken from each

| Source | What is taken |
|---|---|
| **Apple** | Restraint, generous whitespace, typography carrying the hierarchy |
| **Linear** | Speed, keyboard-first operation, dense information without clutter |
| **Notion** | Content-first layout, calm defaults |
| **Raycast** | Command-driven interaction, minimal chrome |
| **Stripe** | Documentation quality, precise data presentation |

---

## Principles

1. **Signal over decoration.** Every visual element earns its place by carrying information.
2. **Typography is the hierarchy.** Size, weight, and spacing structure a page — not boxes,
   borders, or colour.
3. **Colour means something.** Colour encodes state and category. It is never applied for
   variety.
4. **Consistent rhythm.** One spacing scale, applied everywhere. Consistency reads as
   quality more than any individual choice.
5. **Accessible by default.** Text meets WCAG AA contrast in both themes. Colour is never
   the sole carrier of meaning.
6. **Dark and light are equals.** Both themes are designed, not derived by inversion.
7. **Quiet at rest.** A dashboard at rest should feel calm. Emphasis is reserved for what
   needs action now.

---

## Token structure

Tokens live in `core/design/` — part of the specification, so surfaces render the same
language.

```
core/design/
├── tokens.yaml       Colour, typography, spacing, radius, elevation
├── semantic.yaml     Meaning-level mappings: status, priority, life area
└── icons.yaml        Iconography and emoji conventions per entity
```

Semantic tokens reference primitives; surfaces reference semantic tokens only. Changing the
colour of "at risk" is then a one-line change everywhere it appears.

---

## Provisional palette

Tuned for contrast in both themes. Values are finalised in Phase 5 against real dashboards.

| Role | Light | Dark |
|---|---|---|
| Accent / primary | `#0A64D6` | `#0A84FF` |
| Secondary | `#4B49C4` | `#5E5CE6` |
| Success / on track | `#248A3D` | `#30D158` |
| Warning / at risk | `#B25000` | `#FF9F0A` |
| Danger / blocked | `#D70015` | `#FF453A` |
| Info | `#0071A4` | `#40C8E0` |
| Highlight | `#8944AB` | `#BF5AF2` |
| Text primary | `#1C1C1E` | `#F2F2F7` |
| Text secondary | `#636366` | `#AEAEB2` |
| Surface | `#FFFFFF` | `#1C1C1E` |
| Surface raised | `#F2F2F7` | `#2C2C2E` |
| Border | `#D1D1D6` | `#3A3A3C` |

The same palette drives the [GitHub label taxonomy](../../.github/labels.yml), so the
repository and the workspace look like one system.

---

## Spacing and type scale

**Spacing** — a 4 px base: `4 · 8 · 12 · 16 · 24 · 32 · 48 · 64`. No arbitrary values.

**Type** — `12 · 14 · 16 · 20 · 24 · 32 · 40`, with weight and size doing the structural
work. Body text sits at 16 px; anything below 14 px is reserved for metadata.

---

## Sections planned for Phase 5

- Full token reference with resolved light and dark values
- Dashboard layout grid and composition rules
- Component specs: metric tile, progress indicator, status pill, review card, timeline
- Data visualisation: chart types, categorical and sequential palettes, axis and legend rules
- Iconography and emoji conventions per entity and life area
- Density modes and information-per-screen budgets
- Accessibility audit: contrast ratios, non-colour encoding, focus states
- Notion-specific implementation notes — what is achievable, and the workarounds where it is not

---

## Related

- [`core/design/README.md`](../../core/design/README.md) — token file format
- [`workspace/dashboards/README.md`](../../workspace/dashboards/README.md) — dashboard composition

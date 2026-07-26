# core/design/ — design tokens

The visual language, expressed as data so that every surface renders the same system.

Tokens live in `core/` rather than `workspace/` because they are vendor-neutral: the same
tokens drive the Notion workspace, the GitHub label taxonomy, and any future surface.

---

## Planned files

| File | Holds |
|---|---|
| `tokens.yaml` | Primitives: the colour palette, type scale, spacing scale, radius, elevation |
| `semantic.yaml` | Meaning-level mappings: `success`, `warning`, `danger`, `neutral`, per-area colour |
| `icons.yaml` | Iconography and emoji conventions per entity and life area |

---

## Two-tier token model

**Primitives** are raw values with no meaning attached:

```yaml
color:
  blue:
    light: "#0A64D6"
    dark: "#0A84FF"
  green:
    light: "#248A3D"
    dark: "#30D158"
```

**Semantic tokens** map meaning onto primitives:

```yaml
semantic:
  on_track: green
  at_risk: orange
  blocked: red
  accent: blue
```

Surfaces reference **semantic tokens only**. Nothing outside this directory contains a hex
value. Recolouring "at risk" everywhere it appears then becomes a one-line change.

---

## Rules

1. **No hex values outside `tokens.yaml`.** Anywhere else is a leak.
2. **Every colour is defined for both themes.** Dark is designed, not derived by inversion.
3. **Text meets WCAG AA contrast** against its intended background, in both themes. Phase 5
   adds a contrast check to the validator.
4. **Colour is never the only signal.** Pair it with an icon, a label, or position.
5. **Fixed scales.** Spacing on a 4 px base (`4 8 12 16 24 32 48 64`); type at
   `12 14 16 20 24 32 40`. No arbitrary values.

---

## Status

⬜ Finalised in **Phase 5** alongside the dashboards, so tokens are tuned against real
layouts rather than in the abstract. The provisional palette is in the
[Design System guide](../../docs/07-design-system/README.md).

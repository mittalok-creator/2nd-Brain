# assets/ — brand and visual artefacts

Committed binary and vector assets: the project mark, icons, cover images, and exported
diagrams.

---

## Contents

| Directory | Holds |
|---|---|
| [`brand/`](brand/README.md) | Logo, wordmark, icon, cover images |
| `diagrams/` | Generated architecture and entity-relationship diagrams *(Phase 4)* |

---

## Rules

1. **SVG wherever possible.** Vector scales, diffs meaningfully, and stays small.
2. **Optimise before committing.** Run PNGs through a compressor; strip SVG editor metadata.
3. **Size limit.** Nothing over 500 KB without good reason — repository weight is permanent.
4. **Both themes.** Any asset appearing on a themed surface ships light and dark variants.
5. **Descriptive filenames.** `architecture-layers-dark.svg`, not `diagram2.svg`.
6. **Generated assets are not hand-edited.** Diagrams produced by a script are regenerated,
   never patched — a hand-edit is lost on the next run.
7. **No screenshots containing personal data.** Documentation screenshots use example content.

---

## Naming

```
<subject>-<variant>-<theme>.<ext>

logo-full-dark.svg
logo-mark-light.svg
architecture-layers-dark.svg
erd-core-light.svg
```

---

## Status

🚧 Structure defined in Phase 1. Brand assets and generated diagrams land in **Phases 4–5**.

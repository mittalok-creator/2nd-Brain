# prompts/library/ — concrete prompts

Ready-to-use prompts for specific, recurring tasks. One file per prompt, named
`kebab-case.md` after the task it performs.

A prompt belongs here rather than in `agents/` when it is invoked directly — by a human in a
chat window, or by an automation — without a full nine-part agent contract behind it.

---

## Organisation

Prompts are named by the task, in verb-object form, so the library reads as a list of things
the system can do:

```
library/
├── extract-actions-from-notes.md
├── summarise-article.md
├── route-inbox-item.md
├── draft-weekly-review.md
├── critique-decision.md
├── generate-project-brief.md
└── classify-expense.md
```

---

## Conventions

- **Verb-object filenames.** `summarise-article.md`, not `article.md` or `summariser.md`.
- **One task per prompt.** A prompt doing three things does none of them predictably.
- **Follow the house standards** in [`prompts/README.md`](../README.md) — output contract,
  model tier, untrusted-content framing, length limit, changelog.
- **Name the pattern** each prompt is built from, so improvements to a pattern can be
  propagated.
- **Record real failures** in the changelog. A prompt's history of what went wrong is the most
  valuable documentation it has.

---

## Status

⬜ Populated in **Phase 6**.

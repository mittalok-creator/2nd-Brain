# automation/recipes/ — automation definitions

The platform-neutral source of truth for every automation. One file per automation, named
`kebab-case.yaml`.

A recipe is reviewable: it states intent, trigger, steps, idempotency strategy, and failure
behaviour in a form a human can read in a diff. A 4,000-line n8n JSON export is not
reviewable, which is why the recipe exists alongside it.

---

## Every recipe declares

| Section | Why it is mandatory |
|---|---|
| `trigger` | When it runs, in an explicit timezone |
| `idempotency` | What happens on a second run for the same period |
| `steps` | The ordered work, readable without opening the platform |
| `on_failure` | Retries, notification, and what state is left behind |
| `observability` | The event emitted, so runs are traceable |

An automation without a declared idempotency strategy is not accepted. Automations re-run —
retries, backfills, manual triggers, timezone edge cases — and non-idempotent automations
produce duplicate tasks and double-counted metrics whose cleanup costs more than the
automation ever saved.

---

## Idempotency strategies

| Strategy | Mechanism | Fits |
|---|---|---|
| `date_scoped_upsert` | One record per date; a second run updates it | Daily and weekly rituals |
| `content_hash` | Skip if a record with the same content hash exists | Capture from feeds and inboxes |
| `external_id` | Key on the source system's id | Calendar events, transactions, emails |
| `run_marker` | Write a marker; refuse to run twice for the same window | Expensive multi-step flows |
| `pure_recompute` | Derive state from scratch every time; no accumulation | Rollups and progress recalculation |

`pure_recompute` is preferred wherever it is affordable — it is idempotent by construction
rather than by discipline.

---

## Naming

Verb-object or ritual name, matching the automation's purpose:

```
recipes/
├── morning-planning.yaml
├── evening-review.yaml
├── weekly-review.yaml
├── track-habits.yaml
├── capture-meeting-notes.yaml
└── classify-expenses.yaml
```

---

## Status

⬜ Populated in **Phase 7**.

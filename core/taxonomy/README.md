# core/taxonomy/ — shared vocabularies

Controlled vocabularies used across many entities. Defining them once here is what makes
cross-domain dashboards possible: a "high priority" task and a "high priority" goal mean the
same thing because they read the same list.

If two entities would otherwise define their own version of the same scale, the scale belongs
here.

---

## Planned vocabularies

| File | Defines |
|---|---|
| `life-areas.yaml` | The top-level domains: health, finance, career, learning, family, growth, meta |
| `statuses.yaml` | Lifecycle states per entity class — task, project, goal, habit |
| `priorities.yaml` | Priority scale with explicit meaning per level |
| `horizons.yaml` | Time horizons: today, week, month, quarter, year, decade |
| `energy.yaml` | Energy cost of work: deep, shallow, admin, recovery |
| `contexts.yaml` | Where or how work happens: desk, phone, errand, offline |
| `sources.yaml` | Where captured information came from: book, article, video, conversation, course |

---

## File format

```yaml
id: priorities
name: Priorities
version: 1.0.0
status: active
owner: core
description: >
  A four-level priority scale. Each level has a definition so that priority is assigned
  by rule rather than by mood.

values:
  - id: critical
    name: Critical
    color: danger              # references core/design/semantic.yaml
    order: 1
    description: Blocks something time-bound. Work on this before anything else.

  - id: high
    name: High
    color: warning
    order: 2
    description: Advances a live goal this week.

  - id: medium
    name: Medium
    color: info
    order: 3
    description: Matters, but not this week.

  - id: low
    name: Low
    color: neutral
    order: 4
    description: Would be nice. Acceptable to never do.
```

---

## Rules

1. **Every value carries a `description`.** An undefined scale gets applied inconsistently
   within a week. The description is the definition, and it is what an agent reads when
   assigning a value.
2. **`order` is explicit.** Never rely on file order or alphabetisation for ranking.
3. **Colour is semantic.** Reference a semantic design token, never a hex value — so
   re-theming is one change.
4. **Values are permanent.** Retire a value with `status: deprecated` rather than deleting
   it; deleted values orphan existing records.
5. **Keep scales short.** Four to six levels. A ten-point scale is never used consistently.

---

## Status

⬜ Populated in **Phase 3**, before the entity schemas that reference it.

# core/relations/ — the relational graph

Relations are declared here, not inside entity schemas. A relation is a fact about *two*
entities; declaring it in one of them would state cardinality twice and let the two copies
disagree.

This directory is what makes 2nd Brain a system rather than a set of unrelated tables.

---

## File format

```yaml
id: goals_to_projects
name: Goals → Projects
version: 1.0.0
status: active
owner: core
description: >
  A goal is delivered through zero or more projects. Every project must serve exactly one
  goal — a project with no goal is unowned work and is surfaced as an exception.

from:
  entity: goals
  field: projects              # the relation property created on goals
  name: Projects
to:
  entity: projects
  field: goal
  name: Goal

cardinality: one_to_many       # one goal, many projects
required_on: to                # a project must have a goal; a goal need not have projects
on_delete: restrict            # refuse to delete a goal that still owns projects

rollups:
  - id: project_count
    on: goals
    over: projects
    aggregate: count

  - id: goal_progress
    on: goals
    over: projects
    field: completion
    aggregate: average
    format: percent
    description: Goal progress is derived from its projects, never entered by hand.
```

---

## Keys

| Key | Meaning |
|---|---|
| `from` / `to` | The two ends: entity, the relation field created on it, and its display name |
| `cardinality` | `one_to_one` · `one_to_many` · `many_to_many` |
| `required_on` | `from` · `to` · `both` · `none` — which side must be populated |
| `on_delete` | `restrict` · `cascade` · `set_null` — behaviour when the owner is removed |
| `rollups` | Derived aggregates carried across the relation |

**Direction convention:** `from` is always the **owner** — the more durable, higher-level
entity. Goals own projects; projects own tasks. Reading `from → to` should read as
"contains" or "is delivered by".

---

## Planned graph

Finalised in Phase 4. The intended shape:

```
        goals ──┬──▶ projects ──▶ tasks
                ├──▶ habits
                ├──▶ finance
                └──▶ health

     knowledge ──┬──▶ projects
                 ├──▶ reading
                 └──▶ resources

       journal ──┬──▶ goals
                 └──▶ decisions

      meetings ──▶ tasks
       reviews ──▶ goals · habits · projects
```

Every entity connects to the graph. An entity with no relations is a note, not part of a
system — that is a signal to reconsider whether it should exist.

---

## Integrity rules

1. **No orphans by default.** If an entity must have an owner, set `required_on`. Orphan
   detection is a validator check from Phase 4.
2. **Derived values are never entered by hand.** Progress, streaks, totals, and counts are
   rollups. A hand-entered progress figure is always wrong eventually.
3. **`many_to_many` needs justification.** It is usually a missing intermediate entity.
4. **No cycles in ownership.** `from → to` must form a directed acyclic graph. Reference
   relations may point anywhere; ownership may not.

---

## Status

⬜ Populated in **Phase 4**, which also generates the entity-relationship diagram committed
to `docs/01-architecture/`.

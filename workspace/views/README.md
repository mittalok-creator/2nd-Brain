# workspace/views/ — reusable database views

A view is a saved question asked of one entity: which rows, in what order, grouped how.

Views are defined once here and referenced by pages and dashboards. Defining a view inline on
a page guarantees that the same question gets asked three slightly different ways.

---

## File format

```yaml
id: tasks_due_today
name: Due Today
version: 1.0.0
status: active
owner: workspace
description: >
  Open tasks due today or overdue, hardest work first. The primary list on the Today page.

entity: tasks
layout: list                    # table | list | board | calendar | timeline | gallery

filter:
  all:
    - { field: status, operator: is_not, value: done }
    - { field: due_date, operator: on_or_before, value: today }

sort:
  - { field: priority, direction: ascending }
  - { field: energy, direction: descending }

properties: [title, project, priority, due_date, energy]

limit: 25
empty_state: Nothing due. Pull forward from This Week, or stop.
```

---

## Keys

| Key | Meaning |
|---|---|
| `entity` | The entity queried — must exist in `core/schema/` |
| `layout` | How rows are presented |
| `filter` | `all` (AND) and/or `any` (OR), nestable |
| `sort` | Ordered list of field and direction |
| `group_by` | Field to group rows by, for board and grouped layouts |
| `properties` | Which fields are visible, in display order |
| `limit` | Maximum rows shown |
| `empty_state` | What to say when there are no rows — always write one |

**Relative date values** — `today`, `tomorrow`, `this_week`, `next_week`, `this_month`,
`past`, `future` — are resolved at render time in `BRAIN_TIMEZONE`. Never hard-code a date.

---

## Conventions

- **Name views by the question they answer**, not by their filter. `stalled_projects`, not
  `projects_filtered_3`.
- **Show only the properties needed to decide.** Every extra column is noise.
- **Always write an `empty_state`.** An empty list with no message reads as a bug; a good
  empty state is often the most useful text on the page.
- **Sort by decision order**, not by creation date. What should be looked at first?
- **Prefer many small views to one configurable one.** A view answering three questions
  answers none of them well.

---

## Status

⬜ Populated in **Phase 5**, alongside the dashboards that compose them. The entities they
query exist as of Phase 3, so the ~60 view ids currently referenced by page blueprints are
forward references until then.

The `workspace/views/` line in the Phase 5 roadmap entry is the plan of record; an earlier note
here said Phase 3, which was wrong.

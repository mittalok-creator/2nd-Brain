# Diary

A separate, chronological log — deliberately **outside** the 2nd Brain specification.

---

## Why this is not part of the system proper

2nd Brain (`core/`, `workspace/`) organises everything by *what it is* — a goal, a task, an
expense. This Diary organises everything by *when it happened*, nothing else. No area, no
relation, no routing gate. That was the explicit request: a simple notebook, not another
structured entity.

Because of that, the Diary:

- has no entity in `core/schema/` and is not in `_catalogue.yaml`,
- has no ADR — it is a request fulfilled, not an architectural decision,
- is not checked by `scripts/validate_repository.py`,
- is recorded in `config/notion.yaml` under a separate `diary:` key, clearly marked as
  outside the specification.

If it turns out to need structure later — linking an entry to a project, say — that is the
point at which it graduates into `core/schema/` with a proper ADR. Until then it stays exactly
what it was asked to be.

---

## Structure

```
📔 Diary
└── 2026
    ├── 📓 Diary Log 2026        one database, every entry in the year
    ├── 01 — January             filtered view: Jan 1–31
    ├── 02 — February            filtered view: Feb 1–28
    ├── …
    └── 12 — December            filtered view: Dec 1–31
```

**One database, twelve filtered views.** Not 366 individual date pages.

A literal page per date was the first reading of the request, and it was rejected on sight:
366 empty pages is nothing to navigate, nothing to scroll past, and no way to see a month at a
glance. A single table with a date-range filter per month gives the same navigation — *2026 →
July → the 27th* — without ever creating an empty page. Every date already has its place, the
moment something is logged against it.

---

## Fields

| Field | Type | For |
|---|---|---|
| **Task** | Title | What was done, or planned |
| **Date** | Date | Which day this belongs to — this is what makes the month views work |
| **Time** | Text | Clock time, e.g. `9:30 AM`. Blank for an all-day entry |
| **Done** | Checkbox | Ticked when finished |
| **Remark** | Text | How it actually went — the line worth re-reading later |

---

## Using it

Open the month, add a row at the bottom. The **Date** field is what sorts it into that month's
view — get the date right and everything else follows automatically.

No monthly setup, no creating "today" first. The row exists the moment it is typed.

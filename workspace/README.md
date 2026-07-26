# workspace/ — the human surface

How the system is **seen and operated**. `core/` declares what exists; `workspace/` declares
how a person navigates it.

Notion is the current surface. This directory is named for the *role*, not the vendor, because
the surface is designed to be replaceable —
see [ADR-0003](../docs/adr/0003-notion-as-projection.md).

---

## Contents

| Path | Declares |
|---|---|
| [`pages/`](pages/README.md) | The page hierarchy and each page's content blueprint |
| [`dashboards/`](dashboards/README.md) | Dashboard compositions — what appears, in what order, why |
| [`views/`](views/README.md) | Reusable view definitions — filters, sorts, groupings |
| [`templates/`](templates/README.md) | Page and entry templates |
| `capture-routing.yaml` | The routing table: how a captured item reaches its owning entity |

---

## Rules

1. **Reference only what exists.** A view or page may only use entities and fields declared
   in `core/`. The validator enforces this from Phase 3.
2. **No structural definitions here.** If it describes *what data is*, it belongs in `core/`.
   This directory describes *how data is presented*.
3. **Composition over duplication.** A dashboard composes existing views. If a dashboard
   needs a new view, add the view and reference it.
4. **Reachability.** Every surface is reachable from Home in two clicks or fewer. A page that
   is not reachable does not get used.
5. **Content-free.** Blueprints describe structure and intent, never real entries.

---

## Structure versus content

| Owned by the repository | Owned by Notion |
|---|---|
| Which pages exist, and their hierarchy | The text you write on them |
| Which views a database has | The rows in that database |
| What a template contains | The entries created from it |
| Dashboard composition | Your actual tasks, notes, and journals |

Structure is versioned. Content is not, and never enters this repository.

---

## Design intent

The workspace targets **low noise and fast operation** — Apple's restraint, Linear's speed.
Concretely, the rules dashboards are held to:

- One primary question per page. If a page answers three questions, it is three pages.
- Nothing on screen that does not inform a decision.
- Live state above reference material; today above this week above this month.
- Every routine action reachable without hunting.

Full language in the [Design System guide](../docs/07-design-system/README.md).

---

## Status

✅ **Phase 2** — page hierarchy, navigation model, and capture routing are settled. Sixteen
page blueprints are written; see
[Information architecture](../docs/01-architecture/information-architecture.md).

⬜ Views land in **Phase 3**, dashboards and templates in **Phase 5**. Page blueprints
therefore contain forward references to views and dashboards that do not exist yet — expected,
and validated when those land.

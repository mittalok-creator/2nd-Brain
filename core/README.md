# core/ — the specification

**This is the system.** Everything else in the repository is a projection of what is declared
here.

`core/` is vendor-neutral by rule. It contains no Notion concepts, no API shapes, and no
implementation detail. The test for whether something belongs here:

> **Would this still be true if Notion disappeared tomorrow?**

If yes, it belongs in `core/`. If it only makes sense because of how a particular tool works,
it belongs in `workspace/` or in a provider adapter.

---

## Contents

| Directory | Declares |
|---|---|
| [`schema/`](schema/README.md) | Entities and their fields — types, defaults, constraints |
| [`relations/`](relations/README.md) | The relational graph — cardinality, ownership, rollups |
| [`taxonomy/`](taxonomy/README.md) | Shared vocabularies — life areas, statuses, priorities, horizons |
| [`design/`](design/README.md) | Design tokens — colour, typography, spacing, iconography |

---

## Rules

1. **`core/` depends on nothing.** No references outward to `workspace/`, `agents/`, or
   `automation/`. Those layers depend on this one, never the reverse.
2. **No vendor types.** Field types are abstract and mapped at sync time.
   See [ADR-0003](../docs/adr/0003-notion-as-projection.md).
3. **Ids are permanent.** A `snake_case` id, once committed, never changes. Display names may
   be renamed freely. See [ADR-0002](../docs/adr/0002-naming-and-versioning.md).
4. **One concept, one file.** An entity is declared in exactly one place.
5. **Every file carries the header contract** — validated in CI.
6. **Structure only, never content.** Columns, not rows. No personal data.

---

## The header contract

Every YAML file in `core/` begins with:

```yaml
id: decisions               # snake_case, permanent
name: Decisions             # Title Case, freely renamable
version: 1.0.0              # semantic
status: active              # draft | active | deprecated
owner: core
description: >
  One sentence explaining what this entity is for.
```

---

## Abstract field types

The complete set. A provider adapter maps each to its vendor equivalent; nothing outside this
list may be used.

| Type | Holds |
|---|---|
| `text` | Short single-line text |
| `rich_text` | Formatted multi-line content |
| `number` | Numeric, with optional `format` (integer, currency, percent) |
| `select` | One value from a defined set |
| `multi_select` | Zero or more values from a defined set |
| `status` | One value from an ordered lifecycle set |
| `date` | Date or datetime, optionally a range |
| `checkbox` | Boolean |
| `url` · `email` · `phone` | Typed strings |
| `relation` | A link to another entity |
| `rollup` | A value aggregated across a relation |
| `formula` | A derived value, declared as an expression |
| `person` | A person reference |
| `file` | An attachment reference |
| `created_time` · `last_edited_time` | System timestamps |

---

## Change process

1. Edit or add the specification here.
2. Update `relations/` if the change affects the graph.
3. Run `make validate`.
4. Commit with the matching scope: `feat(schema): …`, `feat(taxonomy): …`.
5. If existing state must migrate, mark the change breaking and write migration notes.

---

## Status

✅ **Phase 3** — 23 entities in `schema/`, 5 shared taxonomies in `taxonomy/`. Field contracts,
taxonomy references, and entity ownership are enforced by `make schema`.

⬜ `relations/` in **Phase 4**, `design/` in **Phase 5**. Schemas carry no `relation` or
`rollup` fields until then, by design — see [ADR-0007](../docs/adr/0007-entity-catalogue-and-normalisation.md).

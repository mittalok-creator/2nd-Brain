# core/schema/ — entity definitions

One file per entity, named `kebab-case.yaml` after the entity's display concept. The
permanent identity is the `id` inside the file.

The index of every entity — its group, purpose, owning page, and defining file — is
[`_catalogue.yaml`](_catalogue.yaml). It also records every entity **considered and rejected**,
with the reason, so the same proposals are not re-litigated.

Before adding an entity, apply the normalisation rule from
[ADR-0007](../../docs/adr/0007-entity-catalogue-and-normalisation.md):

> **Merge when the field sets are the same. Separate when they diverge.**

---

## File format

```yaml
id: decisions
name: Decisions
version: 1.0.0
status: active
owner: core
description: >
  A record of significant decisions, their reasoning, and their eventual outcomes,
  used to calibrate future judgement.

icon: "⚖️"
area: meta                      # references core/taxonomy/life-areas.yaml

fields:
  - id: title
    name: Decision
    type: text
    required: true
    description: The decision, phrased as a statement.

  - id: decided_on
    name: Decided On
    type: date
    required: true

  - id: confidence
    name: Confidence
    type: number
    format: percent
    validation:
      min: 0
      max: 100
    description: Confidence at the time of deciding, recorded before the outcome is known.

  - id: reversibility
    name: Reversibility
    type: select
    options: [reversible, costly_to_reverse, irreversible]
    default: reversible

  - id: expected_outcome
    name: Expected Outcome
    type: rich_text
    required: true

  - id: actual_outcome
    name: Actual Outcome
    type: rich_text
    description: Filled in at review time, not at decision time.

  - id: review_on
    name: Review On
    type: date
    description: When to compare expectation against reality.

identity:
  primary: title
  slug_from: [title, decided_on]

defaults:
  sort: [{ field: decided_on, direction: descending }]
```

---

## Field keys

| Key | Required | Meaning |
|---|---|---|
| `id` | yes | `snake_case`, permanent |
| `name` | yes | Title Case display label |
| `type` | yes | One of the abstract types in [`core/README.md`](../README.md) |
| `required` | no | Defaults to `false` |
| `description` | no | Why the field exists — strongly encouraged |
| `default` | no | Applied on creation |
| `options` | for `select`/`multi_select`/`status` | Allowed values, `snake_case` |
| `format` | for `number` | `integer` · `decimal` · `currency` · `percent` |
| `validation` | no | `min`, `max`, `pattern`, `max_length` |
| `unit` | no | Display unit, e.g. `kg`, `minutes` |
| `computed` | no | `formula` or `rollup` expression |

Relations are **not** declared here. They live in
[`core/relations/`](../relations/README.md) so the graph has a single home and cardinality is
stated once rather than twice.

---

## Conventions

- Order fields as a human would fill them: identity, then core attributes, then metadata.
- Give every non-obvious field a `description`. It becomes the tooltip in the workspace and
  the context an agent reads.
- Prefer `select` over free `text` wherever a value is one of a known set — enums are what
  make dashboards possible.
- Reuse taxonomy values instead of redefining a status or priority scale per entity.
- Keep entities normalised: if a group of fields repeats across entities, it is probably its
  own entity.

---

## Enforcement

`make schema` checks that every field uses an abstract type, that enum fields resolve to a
taxonomy or declare a local option list, that defaults are allowed values, that
`identity.primary` and `slug_from` name real fields, that no `relation` or `rollup` appears
here, and that every entity is catalogued and owned by exactly one page.

---

## Status

✅ **Phase 3** — 23 entities defined. Relations arrive in **Phase 4**.

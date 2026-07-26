# ADR-0001 — Four-layer architecture

| | |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-07-26 |
| **Phase** | Phase 1 — Repository Architecture |
| **Supersedes** | — |
| **Superseded by** | — |

## Context

The initial plan for the repository proposed a flat layout with sibling top-level
directories: `/notion`, `/databases`, `/templates`, `/agents`, `/prompts`, `/automation`,
`/scripts`, `/assets`, `/workflows`, `/config`.

Working through what each directory would actually contain surfaced three problems:

1. **Overlapping concepts.** `/databases` would hold database definitions and `/notion`
   would hold the Notion representation of those same databases — two homes for one
   concept, guaranteed to drift. `/templates` had the same relationship with `/notion`.
   `/workflows` and `/automation` were two names for the same thing.

2. **No dependency direction.** With ten peer directories there is no stated rule about
   what may reference what. Over time everything references everything, and no part can be
   replaced independently.

3. **Vendor coupling by structure.** A top-level `/notion` directory encodes the assumption
   that Notion is the system. It is a surface, and surfaces get replaced.

The system needs to survive years of tool churn, and needs to remain comprehensible when
returned to after months away.

## Decision

Organise the repository into **four layers with an inward dependency rule**.

| Layer | Directory | Responsibility |
|---|---|---|
| **Specification** | `core/` | What exists: entities, fields, relations, taxonomy, design tokens |
| **Surface** | `workspace/` | How a human sees it: pages, dashboards, views, templates |
| **Intelligence** | `agents/`, `prompts/` | How the system thinks |
| **Execution** | `automation/` | How the system runs itself |

Supporting directories (`scripts/`, `config/`, `docs/`, `assets/`, `tests/`) are
infrastructure and sit outside the layer model.

**Dependency rule:** dependencies point inward toward `core/`. `core/` depends on nothing.
`workspace/`, `agents/`, and `automation/` each depend on `core/` and must not depend on
one another directly; they coordinate through the data model.

Consequent renames and merges:

| Proposed | Becomes | Reason |
|---|---|---|
| `/notion` | `workspace/` | The surface is a role, not a vendor. See ADR-0003. |
| `/databases` | `core/schema/` | Database definitions *are* the specification |
| `/templates` | `workspace/templates/` | Templates are a surface concern |
| `/workflows` | `automation/` | Duplicate concept; one name for one thing |

## Alternatives considered

### The originally proposed flat layout

Simple to read at a glance, and familiar. Rejected because it has no dependency rule, and
because two directories owning "databases" and two owning "templates" would drift within
weeks. Flat layouts work when directories are genuinely independent; these are not.

### Domain-first layout (`/health`, `/finance`, `/career`, …)

Group everything about a life area together: its schema, dashboards, agents, automations.
Attractive because it matches how the system is *used*.

Rejected because it fragments every cross-cutting concern. A change to the task schema
would touch ten directories; the relational graph — the thing that makes this a system
rather than ten silos — would have no home. Life areas are already modelled properly as a
taxonomy in `core/taxonomy/`, which is where that grouping belongs.

### Single `src/` with internal modules

Conventional for software. Rejected because this repository is predominantly a
specification and documentation artefact, not an application. A `src/` directory would
imply compiled output and hide the fact that the specification is the deliverable.

## Consequences

**Positive**

- Any surface can be replaced without touching the specification.
- The dependency rule is checkable, and gives reviewers an objective test.
- New entities, agents, and automations slot into an existing home — additions do not
  require restructuring.
- One concept has exactly one location, removing the main source of drift.

**Negative**

- Adding one entity end to end touches three directories (`core/schema/`,
  `core/relations/`, `workspace/views/`) rather than one. Accepted: the alternative is
  duplication.
- `core/` versus `workspace/` requires a judgement call for a small number of files. The
  test: *would this still be true if Notion disappeared?* If yes, it belongs in `core/`.

**Neutral / accepted trade-offs**

- More indirection than a flat layout. Justified by the replaceability it buys.
- Directory names diverge from the original plan. Documented here and in `CHANGELOG.md`.

## Revisit when

- A second surface (mobile app, local mirror, alternative workspace tool) is built and the
  `workspace/` layer turns out to need per-surface subdivision.
- The dependency rule is violated three times for good reasons — that would indicate the
  layer boundaries are drawn in the wrong place.

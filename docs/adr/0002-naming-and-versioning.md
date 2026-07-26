# ADR-0002 — Naming and versioning conventions

| | |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-07-26 |
| **Phase** | Phase 1 — Repository Architecture |
| **Supersedes** | — |
| **Superseded by** | — |

## Context

The system will accumulate dozens of entities, agents, views, and automations, authored
across long gaps in time and by both a human and AI agents. Two failure modes are close to
certain without an explicit convention:

1. **Naming drift.** `decision_journal`, `decisionJournal`, `Decision-Journal`, and
   `decisions` all appearing as references to the same thing. Cross-layer references break
   silently, and search stops working.

2. **Rename breakage.** Display names are the names most likely to change — "Reading"
   becomes "Reading & Media", "Knowledge" becomes "Knowledge Base". If display names double
   as identifiers, every rename becomes a migration across schema, views, agents, prompts,
   and automations.

There is also no obvious answer to what "version 2.0" of a personal operating system means,
since the repository is not a published package.

## Decision

### Identity is separate from display

Every specification object carries a stable `id` **and** a human `name`. The `id` is
permanent; the `name` is free to change at any time.

| Thing | Convention | Example |
|---|---|---|
| Directory | `kebab-case` | `core/schema/` |
| Specification file | `kebab-case.yaml` | `decision-journal.yaml` |
| Entity id | `snake_case` | `decision_journal` |
| Field id | `snake_case` | `expected_outcome` |
| Display name | Title Case | `Decision Journal` |
| Agent id | `kebab-case` | `personal-ceo` |
| Enum value | `snake_case` | `in_progress` |
| Documentation file | `kebab-case.md` | `system-architecture.md` |
| ADR file | `NNNN-kebab-case.md` | `0002-naming-and-versioning.md` |

Two casing styles are used deliberately: `snake_case` for anything that behaves like a
data field, `kebab-case` for anything that behaves like a path. The style of an identifier
therefore tells you what kind of thing it is.

**Ids are permanent.** Changing an id is a breaking change requiring a migration note. The
filename tracks the display concept; the `id` inside the file is the contract.

### Every specification file carries a header

```yaml
id: decision_journal
name: Decision Journal
version: 1.0.0
status: active        # draft | active | deprecated
owner: core
description: >
  One sentence explaining what this entity is for.
```

The validator enforces the presence of these fields, semantic `version`, and a valid
`status`. Files under a `_`-prefixed path (templates, registries, indexes) are exempt.

### Versioning is applied to the specification

Semantic versioning, interpreted for a specification rather than a library:

| Bump | Means |
|---|---|
| **MAJOR** | A breaking change to the data model or page hierarchy; existing state must be migrated |
| **MINOR** | New entities, agents, dashboards, or automations, added backwards-compatibly |
| **PATCH** | Documentation, copy, tuning, and fixes with no structural impact |

Individual specification files version independently in their header. The repository
versions as a whole via git tags, one minor release per completed phase, reaching `v1.0.0`
at the end of Phase 9.

### Commits are conventional

[Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/), with scopes drawn
from the top-level directories. Enforced in CI on pull requests. Full list in
[`CONTRIBUTING.md`](../../CONTRIBUTING.md).

## Alternatives considered

### One casing style everywhere

Simpler to remember. Rejected because the dual style carries information at zero cost:
seeing `in_progress` versus `personal-ceo` immediately tells you whether you are looking at
a data value or a path segment.

### Display names as identifiers

Removes the `id`/`name` distinction and the duplication that comes with it. Rejected
because renaming is frequent and near-costless under the chosen scheme, and catastrophic
under this one. The duplication is small and pays for itself the first time something is
renamed.

### Date-based versioning (`2026.07`)

Honest about a system that evolves continuously rather than shipping releases. Rejected
because it carries no information about whether an update breaks existing state — which is
the single most important thing to know before pulling a change into a live workspace.

### No versioning at all

Defensible for a personal repository. Rejected because migrations across a live Notion
workspace need a reference point, and because the changelog needs anchors.

## Consequences

**Positive**

- Cross-layer references are mechanically predictable and machine-checkable.
- Renaming anything user-facing is a one-line change.
- A version number communicates migration risk at a glance.
- AI agents contributing to the repository have an unambiguous rule to follow, removing the
  most common source of inconsistency.

**Negative**

- Every specification object carries both an `id` and a `name`. Mild redundancy, accepted.
- Contributors must remember which casing applies where. Mitigated by the table above, the
  header contract, and validator enforcement.

**Neutral / accepted trade-offs**

- Semantic versioning is a slightly loose fit for a specification. The MAJOR/MINOR/PATCH
  meanings are redefined above rather than borrowed, which is enough.

## Revisit when

- A third casing style is genuinely needed for a new class of object.
- Phase 9 shows that per-file `version` headers are not being maintained honestly, in which
  case drop them in favour of repository-level versioning alone.

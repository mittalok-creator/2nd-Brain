# ADR-0008 — Stable identity and slugs

| | |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-07-26 |
| **Phase** | Phase 3 — Databases |
| **Supersedes** | — |
| **Superseded by** | — |

## Context

The same record has to be referenceable from four places that do not share an identifier
space:

- the **repository** — a schema, a routing rule, or an automation recipe naming a record,
- **Notion** — which assigns opaque UUIDs on creation,
- **agents** — which receive records as context and must refer to them in output,
- **automations** — which must decide whether an incoming item is new or already present.

Notion's page id is the obvious candidate and fails on three counts. It does not exist until
after creation, so nothing can reference a record it is about to create. It is not reproducible
— rebuilding the workspace assigns entirely new ids, invalidating every stored reference. And
it is unreadable, so a reference in a diff or an agent's output conveys nothing.

The related problem is idempotency. Every automation must be able to answer "have I already
recorded this?" without a UUID, since the source system does not know Notion's ids. Without a
stated answer, each automation invents its own and the duplicate-record failures documented in
ADR-0006 return in a different form.

ADR-0002 established that entity and field **ids** are permanent and display names are free to
change. It did not establish how individual **records** are identified.

## Decision

**Three layers of identity, each for a different job.**

| Layer | What it is | Job |
|---|---|---|
| **Type id** | `snake_case` entity and field id | Names the *shape*. Permanent. (ADR-0002) |
| **Slug** | Derived, human-readable record key | Names the *record*, portably and reproducibly |
| **Provider id** | Notion's UUID | Addresses the record inside one provider. Deployment state. |

### Slugs

Every schema declares an `identity` block:

```yaml
identity:
  primary: title            # the field a human reads to recognise the record
  slug_from: [decided_on, title]
```

`slug_from` names the fields the slug is built from, in order. Generation: take each field's
value, lowercase it, replace non-alphanumerics with hyphens, collapse repeats, join with
hyphens, truncate.

```
decided_on: 2026-03-14, title: "Move the team to trunk-based development"
→ 2026-03-14-move-the-team-to-trunk-based-development
```

Slugs are **derived, not stored as the source of truth**. Editing a title changes the slug —
which is correct, because a slug is a readable handle rather than a database key. Where a
durable handle is needed the provider id is used, and where a *reproducible* handle is needed
the slug is recomputed.

### Choosing `slug_from`

The rule is uniqueness in practice, not uniqueness in theory:

| Entity | `slug_from` | Why |
|---|---|---|
| `goals` | `area`, `title` | Titles are distinctive; area disambiguates across domains |
| `tasks` | `created_at`, `title` | Task titles repeat legitimately — "draft the summary" recurs |
| `journal` | `entry_date` | One entry per day; the date *is* the identity |
| `transactions` | `transaction_date`, `description`, `amount` | Any two of these collide; all three rarely do |
| `health_metrics` | `measured_on`, `metric` | One reading per metric per day |
| `habit_logs` | `period_date` | Unique within its habit, supplied by the relation |

Where the natural key genuinely repeats, a timestamp is included rather than pretending the
title is unique. Pretending is what produces silent overwrites.

### Uniqueness keys and idempotency

Some entities have a **uniqueness key** distinct from the slug — the tuple an automation uses
to decide update-versus-create:

| Entity | Uniqueness key | Used by |
|---|---|---|
| `journal` | `entry_date` | Evening Review |
| `reviews` | `review_type`, `period_start` | Weekly and Monthly Review |
| `habit_logs` | habit, `period_date` | Habit Tracking |
| `health_metrics` | `metric`, `measured_on` | Health import |
| `budgets` | `category`, `period_type`, `period_start` | Budget setup |
| `meetings` | `external_event_id` | Meeting Notes |
| `transactions` | `external_id` | Expense import |

This is the concrete mechanism behind the idempotency requirement in ADR-0006 and
`automation/README.md`. An automation whose entity has a uniqueness key upserts on it; one
whose entity has none must declare a different strategy.

**Where an external system supplies an id, it wins.** `meetings.external_event_id` and
`transactions.external_id` take precedence over any derived key, because the source system's
notion of identity is authoritative for records it originates.

### Provider ids are deployment state

Notion page and database ids are held in `config/notion.yaml`, git-ignored where they point at
private content. They never appear in `core/` or `workspace/`. A provider id is a fact about
one installation, not part of the specification.

## Alternatives considered

### Notion page ids as the only identity

Simplest — no derivation, guaranteed unique, already exists. Rejected for the three reasons in
Context: unavailable before creation, not reproducible across a rebuild, and unreadable in a
diff or an agent's output. It also couples `core/` to a vendor, which ADR-0003 forbids.

### A generated UUID stored on every record

Reproducible if stored, unique, no collision handling. Rejected because it solves identity
while solving nothing else: it is as unreadable as Notion's id, and it does not help
idempotency at all — an automation still cannot compute the UUID of a record it has not seen.

### Content hash as the record key

Deterministic, no collisions, and idempotent by construction. Genuinely attractive for capture
pipelines.

Rejected as a general scheme because the key changes whenever any field changes, so every edit
looks like a new record. It remains available as a *strategy* for capture-from-feed automations,
where immutability is a reasonable assumption, and is listed as such in
`automation/recipes/README.md`.

### Sequential numbers per entity

Readable, short, stable. Rejected because assigning the next number requires a global read
before every write, which is a race condition in any concurrent automation and a needless
round trip in every other case.

### No slugs — display names only

Least machinery. Rejected because display names are the values most likely to change, and using
them as references makes every rename a broken link across schemas, routing rules, and prompts.

## Consequences

**Positive**

- A record can be referenced before it exists, which is what makes routing rules and
  automation recipes writable.
- The whole workspace is reproducible: rebuilding regenerates the same slugs.
- References are readable in diffs, prompts, and agent output.
- Idempotency has one stated mechanism instead of one per automation.
- External ids are respected where they exist, so imports converge rather than duplicate.

**Negative**

- Slugs change when their source fields change. Acceptable because a slug is a handle, not a
  key; anything needing durability uses the provider id.
- Collisions remain possible in principle — two tasks created in the same second with the same
  title. Resolved by appending a discriminator at creation; the resulting id is then permanent.
- `identity` must be declared on every schema. Enforced by the validator, which checks that
  `primary` and every `slug_from` field actually exists.

**Neutral / accepted trade-offs**

- Three identity layers is more than one. Each has a distinct job, and collapsing any two
  reintroduces a problem the split solves.
- Slug generation must be implemented identically in the sync adapter and in any automation
  that computes one. Centralised in `scripts/` when the adapter is built in a later phase.

## Revisit when

- Slug collisions occur often enough to need a general strategy rather than per-case
  disambiguation.
- An entity turns out to need a durable, human-readable key that survives edits, which would
  argue for a stored slug with the derived one as a fallback.
- A second provider is added, at which point the provider-id layer needs a namespace.
